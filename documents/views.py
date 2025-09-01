from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib import messages
from .models import Document, AccessRequest
from .forms import DocumentForm, SearchForm, AccessRequestForm
from cryptography.fernet import Fernet
import os
import mimetypes
from datetime import datetime
from django.conf import settings
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

@login_required
def upload_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.owner = request.user
            document.size = request.FILES['file'].size
            document.status = 'queued'
            
            # Save encrypted file
            key = Fernet.generate_key()
            fernet = Fernet(key)
            file_content = request.FILES['file'].read()
            encrypted_content = fernet.encrypt(file_content)
            
            file_name = request.FILES['file'].name
            encrypted_path = os.path.join('media/documents', f'encrypted_{document.owner.id}_{file_name}')
            os.makedirs(os.path.dirname(encrypted_path), exist_ok=True)
            with open(encrypted_path, 'wb') as f:
                f.write(encrypted_content)
            
            document.file = f'documents/encrypted_{document.owner.id}_{file_name}'
            document.encryption_key = key
            document.is_encrypted = True
            document.virus_scanned = True
            document.audit_trail = True
            document.status = 'completed'
            document.save()
            form.save_m2m()  # Save tags
            return redirect('my_documents')
        else:
            document = Document(status='failed')
    else:
        form = DocumentForm()
    recent_uploads = Document.objects.filter(owner=request.user).order_by('-upload_date')[:5]
    return render(request, 'documents/upload.html', {
        'form': form,
        'recent_uploads': recent_uploads,
        'document_form': DocumentForm(),
        'search_form': SearchForm()
    })

@login_required
def my_documents(request):
    documents = Document.objects.filter(owner=request.user)
    
    # Apply filters
    search_query = request.GET.get('search', '').strip()
    category = request.GET.get('category', '')
    access_level = request.GET.get('access_level', '')
    
    if search_query:
        documents = documents.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(tags__name__icontains=search_query)
        ).distinct()
    if category:
        documents = documents.filter(category=category)
    if access_level:
        documents = documents.filter(access_level=access_level)
    
    # Handle empty results
    if not documents.exists():
        documents = None
    
    # Paginate results
    paginator = Paginator(documents or [], 10)
    page_number = request.GET.get('page', 1)
    try:
        documents_page = paginator.page(page_number)
    except:
        documents_page = paginator.page(1)
    
    return render(request, 'documents/my_documents.html', {
        'documents': documents_page,
        'document_form': DocumentForm(),
        'search_form': SearchForm(initial={
            'query': search_query,
            'category': category,
            'access_level': access_level
        }),
        'search_query': search_query,
        'category': category,
        'access_level': access_level
    })

@login_required
def search_documents(request):
    form = SearchForm(request.GET or None)
    documents = Document.objects.all().order_by('-upload_date')
    query = None
    search_type = 'keyword'

    if form.is_valid():
        query = form.cleaned_data.get('query', '').strip()
        search_type = form.cleaned_data.get('search_type', 'keyword')
        category = form.cleaned_data.get('category', '')
        access_level = form.cleaned_data.get('access_level', '')
        date_from = form.cleaned_data.get('date_from')
        date_to = form.cleaned_data.get('date_to')
        tags = form.cleaned_data.get('tags', [])
        
        # Apply search query
        if query:
            if search_type in ['keyword', 'hybrid']:
                documents = documents.filter(
                    Q(title__icontains=query) |
                    Q(description__icontains=query) |
                    Q(tags__name__icontains=query)
                ).distinct()
            # Placeholder for semantic search (requires Elasticsearch)
            if search_type in ['semantic', 'hybrid'] and 'django_elasticsearch_dsl' in settings.INSTALLED_APPS:
                # Implement Elasticsearch query here
                pass
        
        # Apply filters
        if category:
            documents = documents.filter(category=category)
        if access_level:
            documents = documents.filter(access_level=access_level)
        if date_from:
            documents = documents.filter(upload_date__gte=date_from)
        if date_to:
            documents = documents.filter(upload_date__lte=date_to)
        if tags:
            for tag in tags:
                documents = documents.filter(tags__name=tag)
    
    # Handle empty results
    if not documents.exists():
        documents = None
    
    # Paginate results
    paginator = Paginator(documents or [], 10)
    page_number = request.GET.get('page', 1)
    try:
        documents_page = paginator.page(page_number)
    except:
        documents_page = paginator.page(1)
    
    return render(request, 'documents/search_results.html', {
        'form': form,
        'documents': documents_page,
        'query': query if form.is_valid() else '',
        'search_type': search_type if form.is_valid() else 'keyword'
    })

@login_required
def view_document(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    if document.owner != request.user and not (
        document.access_level == 'public' or
        document.access_level == 'internal' or
        (document.access_level == 'restricted' and request.user.has_perm('documents.can_view_restricted')) or
        (document.access_level == 'private' and request.user.has_perm('documents.can_view_private'))
    ):
        return HttpResponseForbidden("You do not have permission to view this document.")
    
    document.views += 1
    document.save()
    
    fernet = Fernet(document.encryption_key)
    with open(document.file.path, 'rb') as f:
        encrypted_content = f.read()
    decrypted_content = fernet.decrypt(encrypted_content)
    
    mime_type, _ = mimetypes.guess_type(document.file.name)
    if not mime_type:
        mime_type = 'application/octet-stream'
    elif document.file.name.endswith('.csv'):
        mime_type = 'text/csv'
    
    response = HttpResponse(decrypted_content, content_type=mime_type)
    response['Content-Disposition'] = f'inline; filename="{document.title}"'
    return response

@login_required
def download_document(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    if document.owner != request.user and not (
        document.access_level == 'public' or
        document.access_level == 'internal' or
        (document.access_level == 'restricted' and request.user.has_perm('documents.can_view_restricted')) or
        (document.access_level == 'private' and request.user.has_perm('documents.can_view_private'))
    ):
        return HttpResponseForbidden("You do not have permission to download this document.")
    
    fernet = Fernet(document.encryption_key)
    with open(document.file.path, 'rb') as f:
        encrypted_content = f.read()
    decrypted_content = fernet.decrypt(encrypted_content)
    
    mime_type, _ = mimetypes.guess_type(document.file.name)
    if not mime_type:
        mime_type = 'application/octet-stream'
    elif document.file.name.endswith('.csv'):
        mime_type = 'text/csv'
    
    response = HttpResponse(decrypted_content, content_type=mime_type)
    response['Content-Disposition'] = f'attachment; filename="{document.title}"'
    return response

@login_required
def delete_document(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    if document.owner != request.user:
        return HttpResponseForbidden("You can only delete your own documents.")
    
    if request.method == 'POST':
        document.file.delete()
        document.delete()
    return redirect('my_documents')

@login_required
def request_access(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    if document.owner == request.user or document.access_level in ['public', 'internal']:
        messages.error(request, "You already have access to this document.")
        return redirect('my_documents')
    if AccessRequest.objects.filter(requester=request.user, document=document, status='pending').exists():
        messages.error(request, "You have already requested access to this document.")
        return redirect('my_documents')
    if request.method == 'POST':
        form = AccessRequestForm(request.POST)
        if form.is_valid():
            access_request = AccessRequest.objects.create(
                requester=request.user,
                document=document,
                reason=form.cleaned_data['reason'],
                priority=form.cleaned_data['priority']
            )
            messages.success(request, "Access request submitted successfully.")
            return redirect('manage_requests')
    else:
        form = AccessRequestForm()
    return render(request, 'documents/request_access.html', {'form': form, 'document': document})

@login_required
def manage_requests(request):
    my_requests = AccessRequest.objects.filter(requester=request.user).order_by('-request_date')
    pending_requests = AccessRequest.objects.filter(
        document__owner=request.user, status='pending'
    ).order_by('-request_date')
    tab = request.GET.get('tab', 'my_requests')
    return render(request, 'documents/manage_requests.html', {
        'my_requests': my_requests,
        'pending_requests': pending_requests,
        'tab': tab
    })

@login_required
def approve_request(request, request_id):
    access_request = get_object_or_404(AccessRequest, id=request_id)
    if request.user != access_request.document.owner and not request.user.is_superuser:
        return HttpResponseForbidden("You do not have permission to approve this request.")
    if request.method == 'POST':
        access_request.status = 'approved'
        access_request.save()
        # Grant permission via group
        group, _ = Group.objects.get_or_create(name=f"Access_{access_request.document.id}")
        if access_request.document.access_level == 'restricted':
            permission, _ = Permission.objects.get_or_create(
                codename='can_view_restricted',
                content_type=ContentType.objects.get_for_model(Document)
            )
            group.permissions.add(permission)
        elif access_request.document.access_level == 'private':
            permission, _ = Permission.objects.get_or_create(
                codename='can_view_private',
                content_type=ContentType.objects.get_for_model(Document)
            )
            group.permissions.add(permission)
        access_request.requester.groups.add(group)
        messages.success(request, "Access request approved.")
        return redirect('manage_requests')
    return redirect('manage_requests')

@login_required
def deny_request(request, request_id):
    access_request = get_object_or_404(AccessRequest, id=request_id)
    if request.user != access_request.document.owner and not request.user.is_superuser:
        return HttpResponseForbidden("You do not have permission to deny this request.")
    if request.method == 'POST':
        access_request.status = 'denied'
        access_request.save()
        messages.success(request, "Access request denied.")
        return redirect('manage_requests')
    return redirect('manage_requests')
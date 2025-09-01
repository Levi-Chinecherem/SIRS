from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from authentication.models import User
from documents.models import Document
from .models import Log
from .forms import LogFilterForm, UserForm
from django.utils import timezone
from django.http import JsonResponse

@login_required
def user_details(request, user_id):
    user = get_object_or_404(User, id=user_id)
    data = {
        'username': user.username,
        'email': user.email,
        'role': user.role,
        'department': user.department,
        'is_active': user.is_active,
    }
    return JsonResponse(data)

@login_required
def user_management(request):
    users = User.objects.all()
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        if user_id:
            user = get_object_or_404(User, id=user_id)
            form = UserForm(request.POST, instance=user)
        else:
            form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User saved successfully.')
            return redirect('user_management')
    else:
        form = UserForm()
    return render(request, 'admin_panel/user_management.html', {'form': form, 'users': users})

@login_required
def deactivate_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = False
    user.save()
    messages.success(request, 'User deactivated successfully.')
    return redirect('user_management')


def admin_required(view_func):
    decorated_view_func = user_passes_test(lambda u: u.role == 'admin')(view_func)
    return decorated_view_func

@login_required
@admin_required
def admin_dashboard(request):
    active_users = User.objects.filter(is_active=True).count()
    total_documents = Document.objects.count()
    recent_searches = Log.objects.filter(log_type='user_activity', description__icontains='search').count()
    security_events = Log.objects.filter(log_type='security', severity='critical').count()
    recent_logs = Log.objects.order_by('-timestamp')[:5]
    return render(request, 'admin_panel/dashboard.html', {
        'active_users': active_users,
        'total_documents': total_documents,
        'recent_searches': recent_searches,
        'security_events': security_events,
        'recent_logs': recent_logs,
    })

@login_required
@admin_required
def user_management(request):
    users = User.objects.all()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User updated successfully.')
            return redirect('user_management')
    else:
        form = UserForm()
    return render(request, 'admin_panel/user_management.html', {'users': users, 'form': form})

@login_required
@admin_required
def system_logs(request):
    form = LogFilterForm(request.GET or None)
    logs = Log.objects.all().order_by('-timestamp')
    if form.is_valid():
        if form.cleaned_data['log_type']:
            logs = logs.filter(log_type=form.cleaned_data['log_type'])
        if form.cleaned_data['severity']:
            logs = logs.filter(severity=form.cleaned_data['severity'])
        if form.cleaned_data['user']:
            logs = logs.filter(user=form.cleaned_data['user'])
        if form.cleaned_data['date_from']:
            logs = logs.filter(timestamp__gte=form.cleaned_data['date_from'])
        if form.cleaned_data['date_to']:
            logs = logs.filter(timestamp__lte=form.cleaned_data['date_to'])
    paginator = Paginator(logs, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.page(page_number)
    return render(request, 'admin_panel/system_logs.html', {'form': form, 'page_obj': page_obj})

@login_required
@admin_required
def security_center(request):
    return render(request, 'admin_panel/security_center.html')

@login_required
@admin_required
def encryption_keys(request):
    return render(request, 'admin_panel/encryption_keys.html')
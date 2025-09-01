import threading
import os
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import ChatMessage
from documents.models import Document
from transformers import pipeline
from django.http import HttpResponseRedirect
from django.urls import reverse

# Define cache directory for Transformers model
TRANSFORMERS_CACHE_DIR = os.path.join(settings.BASE_DIR, 'cache', 'transformers')
os.makedirs(TRANSFORMERS_CACHE_DIR, exist_ok=True)

# Global variable to store the NLP pipeline
NLP_PIPELINE = None
NLP_LOADING_ERROR = None

# Background model loading function
def load_model():
    global NLP_PIPELINE, NLP_LOADING_ERROR
    try:
        # Initialize Hugging Face Transformers pipeline with cache
        NLP_PIPELINE = pipeline(
            'text-classification',
            model='distilbert-base-uncased',
            cache_dir=TRANSFORMERS_CACHE_DIR
        )
    except Exception as e:
        NLP_LOADING_ERROR = str(e)

# Start model loading in a background thread during module import
model_thread = threading.Thread(target=load_model)
model_thread.daemon = True  # Daemon thread to avoid blocking server shutdown
model_thread.start()

@login_required
def chat_interface(request):
    messages = ChatMessage.objects.filter(user=request.user).order_by('timestamp')[:20]
    recent_chats = ChatMessage.objects.filter(user=request.user, is_user=True).order_by('-timestamp')[:5]
    
    return render(request, 'chat/chat.html', {
        'messages': messages,
        'recent_chats': recent_chats,
    })

@login_required
def send_message(request):
    if request.method == 'POST':
        message_content = request.POST.get('message', '').strip()
        if message_content:
            # Save user message
            user_message = ChatMessage.objects.create(
                user=request.user,
                content=message_content,
                is_user=True
            )

            # Process query using NLP
            try:
                if NLP_LOADING_ERROR:
                    raise Exception(f"Model loading failed: {NLP_LOADING_ERROR}")
                if NLP_PIPELINE is None:
                    raise Exception("NLP model is still loading. Please try again in a moment.")

                # Simple keyword extraction (for demo purposes)
                keywords = message_content.lower().split()

                # Search documents with permission filter
                documents = Document.objects.filter(
                    Q(title__icontains=keywords[0]) |
                    Q(description__icontains=keywords[0]) |
                    Q(tags__name__icontains=keywords[0])
                ).filter(
                    Q(owner=request.user) |
                    Q(access_level='public') |
                    Q(access_level='restricted', owner__groups__permissions__codename='can_view_restricted') |
                    Q(access_level='private', owner__groups__permissions__codename='can_view_private')
                ).distinct()[:3]

                # Generate AI response
                doc_count = documents.count()
                response_content = f"I found {doc_count} document{'s' if doc_count != 1 else ''} matching your query:"
                if doc_count == 0:
                    response_content = "No documents found matching your query. Try refining your search."

                # Save AI response
                ai_message = ChatMessage.objects.create(
                    user=request.user,
                    content=response_content,
                    is_user=False
                )
                ai_message.documents.set(documents)
            except Exception as e:
                ai_message = ChatMessage.objects.create(
                    user=request.user,
                    content=f"Sorry, I encountered an error processing your query: {str(e)}. Please try again.",
                    is_user=False
                )

        return HttpResponseRedirect(reverse('chat_interface'))
    
    return redirect('chat_interface')
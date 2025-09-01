from django.db import models
from django.conf import settings
from documents.models import Document

class ChatMessage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    is_user = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    documents = models.ManyToManyField(Document, blank=True, related_name='chat_messages')

    def __str__(self):
        return f"{self.user.username}: {self.content} ({'User' if self.is_user else 'AI'})"
from django.db import models
from django.conf import settings

class Log(models.Model):
    LOG_TYPES = [
        ('security', 'Security Event'),
        ('user_activity', 'User Activity'),
        ('document_operation', 'Document Operation'),
        ('system_error', 'System Error'),
    ]
    SEVERITY_LEVELS = [
        ('info', 'Info'),
        ('warning', 'Warning'),
        ('critical', 'Critical'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    log_type = models.CharField(max_length=20, choices=LOG_TYPES)
    severity = models.CharField(max_length=20, choices=SEVERITY_LEVELS)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return f"{self.timestamp} - {self.log_type} - {self.severity}"
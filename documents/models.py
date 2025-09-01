from django.db import models
from django.conf import settings
from taggit.managers import TaggableManager
from django.core.validators import FileExtensionValidator

class Document(models.Model):
    ACCESS_LEVELS = (
        ('private', 'Private (Only you)'),
        ('restricted', 'Restricted (Approved users)'),
        ('internal', 'Internal (Organization)'),
        ('public', 'Public (All users)'),
    )
    
    CATEGORIES = (
        ('report', 'Research Reports'),
        ('financial', 'Financial Documents'),
        ('policy', 'Policy Papers'),
        ('manual', 'Technical Manuals'),
        ('legal', 'Legal Documents'),
        ('marketing', 'Marketing Materials'),
        ('training', 'Training Resources'),
        ('other', 'Other'),
    )
    
    DEPARTMENTS = (
        ('engineering', 'Engineering'),
        ('rnd', 'Research & Development'),
        ('finance', 'Finance'),
        ('legal', 'Legal'),
        ('marketing', 'Marketing'),
        ('hr', 'Human Resources'),
        ('operations', 'Operations'),
        ('it', 'IT & Security'),
        ('none', 'None'),
    )
    
    STATUS_CHOICES = (
        ('queued', 'Queued'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )
    
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='documents'
    )
    title = models.CharField(max_length=255)
    file = models.FileField(
        upload_to='documents/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'txt', 'xls', 'xlsx', 'ppt', 'pptx', 'csv'])]
    )
    size = models.BigIntegerField()
    category = models.CharField(max_length=50, choices=CATEGORIES, default='other')
    access_level = models.CharField(max_length=20, choices=ACCESS_LEVELS, default='private')
    department = models.CharField(max_length=50, choices=DEPARTMENTS, default='none', blank=True)
    description = models.TextField(blank=True)
    tags = TaggableManager(blank=True)
    encryption_key = models.BinaryField()
    upload_date = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='queued')
    
    # Security settings
    is_encrypted = models.BooleanField(default=True)
    semantic_indexing = models.BooleanField(default=True)
    auto_keyword_extraction = models.BooleanField(default=True)
    virus_scanned = models.BooleanField(default=True)
    watermarked = models.BooleanField(default=False)
    audit_trail = models.BooleanField(default=True)
    
    class Meta:
        permissions = [
            ('can_view_restricted', 'Can view restricted documents'),
            ('can_view_private', 'Can view private documents'),
        ]

    def __str__(self):
        return self.title

class AccessRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('denied', 'Denied'),
    ]
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High'),
    ]
    requester = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='access_requests'
    )
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name='access_requests'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    request_date = models.DateTimeField(auto_now_add=True)
    reason = models.TextField(blank=True)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='normal')

    def __str__(self):
        return f"{self.requester} requests {self.document}"
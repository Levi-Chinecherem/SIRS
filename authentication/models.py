from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom User model extending AbstractUser
class User(AbstractUser):
    # Define role choices for the user
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('data_owner', 'Data Owner'),
        ('general_user', 'General User'),
    )
    
    # Custom fields
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='general_user')  # User role
    department = models.CharField(max_length=100, blank=True, null=True)  # User's department (optional)
    avatar_initials = models.CharField(max_length=5, blank=True, null=True)  # Auto-generated initials

    # Override save method to generate avatar initials automatically
    def save(self, *args, **kwargs):
        if not self.avatar_initials:  # If initials are not set
            # Generate initials from full name (e.g., "John Doe" -> "JD")
            self.avatar_initials = ''.join([name[0].upper() for name in self.get_full_name().split()])
        super().save(*args, **kwargs)  # Call the parent save method
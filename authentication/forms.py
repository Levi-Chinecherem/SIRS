from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

# Form for user registration
class RegistrationForm(UserCreationForm):
    role = forms.ChoiceField(choices=User.ROLE_CHOICES)  # Dropdown for role selection
    department = forms.CharField(required=False)  # Optional department field

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'role', 'department', 'password1', 'password2')

# Form for user login
class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')
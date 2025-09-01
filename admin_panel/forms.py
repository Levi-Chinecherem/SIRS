from django import forms
from .models import Log
from authentication.models import User

class LogFilterForm(forms.Form):
    LOG_TYPES = Log.LOG_TYPES + [('', 'All Logs')]
    SEVERITY_LEVELS = Log.SEVERITY_LEVELS + [('', 'All Levels')]
    log_type = forms.ChoiceField(choices=LOG_TYPES, required=False, label='Log Type')
    severity = forms.ChoiceField(choices=SEVERITY_LEVELS, required=False, label='Severity')
    user = forms.ModelChoiceField(queryset=User.objects.all(), required=False, label='User')
    date_from = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), label='Date From')
    date_to = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), label='Date To')

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'department', 'is_active']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
            'email': forms.EmailInput(attrs={'class': 'w-full p-2 border rounded'}),
            'role': forms.Select(attrs={'class': 'w-full p-2 border rounded'}),
            'department': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'w-4 h-4'}),
        }
from django import forms
from .models import Document
from taggit.forms import TagField
from django.core.validators import FileExtensionValidator

class DocumentForm(forms.ModelForm):
    file = forms.FileField(
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'txt', 'xls', 'xlsx', 'ppt', 'pptx', 'csv'])],
        help_text="Supports PDF, DOC, DOCX, TXT, XLS, XLSX, PPT, PPTX, CSV files up to 100MB."
    )
    tags = TagField(required=False, help_text="Enter tags separated by commas.")
    semantic_indexing = forms.BooleanField(required=False, initial=True, label="Semantic Indexing")
    auto_keyword_extraction = forms.BooleanField(required=False, initial=True, label="Auto Keyword Extraction")
    watermarked = forms.BooleanField(required=False, initial=False, label="Digital Watermarking")
    
    class Meta:
        model = Document
        fields = ['title', 'file', 'category', 'access_level', 'department', 'description', 'tags', 'semantic_indexing', 'auto_keyword_extraction', 'watermarked']
        
    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            if file.size > 100 * 1024 * 1024:  # 100MB limit
                raise forms.ValidationError("File size exceeds 100MB limit.")
        return file

class SearchForm(forms.Form):
    SEARCH_TYPES = (
        ('keyword', 'Keyword'),
        ('semantic', 'Semantic'),
        ('hybrid', 'Hybrid'),
    )
    
    query = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Search documents...'}),
        label='Search Query'
    )
    search_type = forms.ChoiceField(
        choices=SEARCH_TYPES,
        required=False,
        initial='keyword',
        label='Search Type'
    )
    category = forms.ChoiceField(
        choices=[('', 'All Categories')] + list(Document.CATEGORIES),
        required=False,
        label='Category'
    )
    access_level = forms.ChoiceField(
        choices=[('', 'All Access Levels')] + list(Document.ACCESS_LEVELS),
        required=False,
        label='Access Level'
    )
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Date From'
    )
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Date To'
    )
    tags = TagField(
        required=False,
        help_text="Enter tags separated by commas."
    )

class AccessRequestForm(forms.Form):
    reason = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'w-full p-2 border rounded', 'rows': 4, 'placeholder': 'Why do you need access to this document?'}),
        help_text="Provide a reason for your access request.",
        required=True
    )
    priority = forms.ChoiceField(
        choices=[('low', 'Low'), ('normal', 'Normal'), ('high', 'High')],
        widget=forms.Select(attrs={'class': 'w-full p-2 border rounded'}),
        initial='normal',
        label='Priority'
    )
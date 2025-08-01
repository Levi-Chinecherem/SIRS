from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_document, name='upload_document'),
    path('my/', views.my_documents, name='my_documents'),
    path('search/', views.search_documents, name='search_documents'),
    path('view/<int:document_id>/', views.view_document, name='view_document'),
    path('download/<int:document_id>/', views.download_document, name='download_document'),
    path('delete/<int:document_id>/', views.delete_document, name='delete_document'),
    path('request-access/<int:document_id>/', views.request_access, name='request_access'),
    path('manage-requests/', views.manage_requests, name='manage_requests'),
    path('approve-request/<int:request_id>/', views.approve_request, name='approve_request'),
    path('deny-request/<int:request_id>/', views.deny_request, name='deny_request'),
]
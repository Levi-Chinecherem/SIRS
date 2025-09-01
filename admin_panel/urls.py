from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('user-management/', views.user_management, name='user_management'),
    path('system-logs/', views.system_logs, name='system_logs'),
    path('security-center/', views.security_center, name='security_center'),
    path('encryption-keys/', views.encryption_keys, name='encryption_keys'),
    path('user-details/<int:user_id>/', views.user_details, name='user_details'),
    path('deactivate-user/<int:user_id>/', views.deactivate_user, name='deactivate_user'),
]
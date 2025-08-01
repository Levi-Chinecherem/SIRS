from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from .forms import LoginForm

# URL patterns for the authentication app
urlpatterns = [
    path('login/', LoginView.as_view(template_name='authentication/login.html', authentication_form=LoginForm), name='login'),  # Login view
    path('register/', views.register, name='register'),  # Register view
    path('dashboard/', views.dashboard, name='dashboard'),  # Dashboard view
    path('logout/', LogoutView.as_view(), name='logout'),  # Logout view
]
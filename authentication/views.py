from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, LoginForm
from django.shortcuts import render, redirect

# View for user registration
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegistrationForm()
    return render(request, 'authentication/register.html', {'form': form})

# View for user login
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = LoginForm()
    return render(request, 'authentication/login.html', {'form': form})

# Protected dashboard view with role-based access
@login_required  # Ensure user is logged in
def dashboard(request):
    if request.user.role != 'admin':  # Redirect non-admins to a home page
        return redirect('home')  # Define 'home' URL later
    return render(request, 'dashboard.html')  # Render dashboard for admins
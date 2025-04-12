from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'user'
            user.save()
            login(request, user)
            return redirect('accounts:home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile_view(request):
    return render(request, 'profile.html')

@login_required
def moderator_view(request):
    if request.user.role != 'moderator':
        raise PermissionDenied
    return render(request, 'moderator.html')

@login_required
def admin_view(request):
    if request.user.role != 'admin':
        raise PermissionDenied
    return render(request, 'admin.html')

def home_view(request):
    return render(request, 'accounts/home.html')

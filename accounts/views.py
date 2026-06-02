from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.views import View
from .forms import RegistrationForm, LoginForm, ProfileUpdateForm, AdminUserForm
from .models import User
from audits.utils import log_action


def lockout_response(request, credentials, *args, **kwargs):
    """Custom lockout page for django-axes"""
    return render(request, 'accounts/lockout.html', status=403)


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            log_action(user, 'USER_REGISTERED', f'New applicant registered: {user.username}')
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, f'Welcome, {user.first_name}! Your account has been created.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            log_action(user, 'USER_LOGIN', f'User logged in: {user.username}')
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            next_url = request.GET.get('next', 'dashboard')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    log_action(request.user, 'USER_LOGOUT', f'User logged out: {request.user.username}')
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            log_action(request.user, 'PROFILE_UPDATED', 'User updated their profile')
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'accounts/profile.html', {'form': form})


# ── Admin user management ──────────────────────────────────────────────────────

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_admin:
            return HttpResponseForbidden('Access denied.')
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required
@admin_required
def manage_users_view(request):
    users = User.objects.all().order_by('-created_at')
    role_filter = request.GET.get('role', '')
    if role_filter:
        users = users.filter(role=role_filter)
    return render(request, 'accounts/manage_users.html', {
        'users': users,
        'role_filter': role_filter,
    })


@login_required
@admin_required
def edit_user_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = AdminUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            log_action(request.user, 'USER_EDITED', f'Admin edited user: {user.username}')
            messages.success(request, f'User {user.username} updated.')
            return redirect('manage_users')
    else:
        form = AdminUserForm(instance=user)
    return render(request, 'accounts/edit_user.html', {'form': form, 'target_user': user})


@login_required
@admin_required
def toggle_user_active(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = not user.is_active
    user.save()
    status = 'activated' if user.is_active else 'deactivated'
    log_action(request.user, 'USER_STATUS_CHANGED', f'Admin {status} user: {user.username}')
    messages.success(request, f'User {user.username} has been {status}.')
    return redirect('manage_users')

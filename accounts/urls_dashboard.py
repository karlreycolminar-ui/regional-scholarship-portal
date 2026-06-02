from django.urls import path
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from applications.models import Application
from scholarships.models import Scholarship
from accounts.models import User
from audits.models import AuditLog


@login_required
def dashboard_view(request):
    user = request.user
    context = {'user': user}

    if user.is_admin:
        context.update({
            'total_users': User.objects.count(),
            'total_scholarships': Scholarship.objects.count(),
            'total_applications': Application.objects.count(),
            'pending_apps': Application.objects.filter(status='pending').count(),
            'approved_apps': Application.objects.filter(status='approved').count(),
            'rejected_apps': Application.objects.filter(status='rejected').count(),
            'recent_logs': AuditLog.objects.order_by('-timestamp')[:10],
            'recent_applications': Application.objects.order_by('-date_submitted')[:5],
        })
        return render(request, 'dashboard/admin_dashboard.html', context)

    elif user.is_reviewer:
        context.update({
            'assigned_apps': Application.objects.filter(status='pending').order_by('-date_submitted'),
            'reviewed_count': Application.objects.exclude(status='pending').count(),
            'pending_count': Application.objects.filter(status='pending').count(),
        })
        return render(request, 'dashboard/reviewer_dashboard.html', context)

    else:
        my_apps = Application.objects.filter(user=user).order_by('-date_submitted')
        context.update({
            'my_applications': my_apps,
            'available_scholarships': Scholarship.objects.filter(is_active=True).order_by('deadline')[:5],
            'pending_count': my_apps.filter(status='pending').count(),
            'approved_count': my_apps.filter(status='approved').count(),
            'rejected_count': my_apps.filter(status='rejected').count(),
        })
        return render(request, 'dashboard/applicant_dashboard.html', context)


def home_redirect(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')


urlpatterns = [
    path('', home_redirect, name='home'),
    path('dashboard/', dashboard_view, name='dashboard'),
]

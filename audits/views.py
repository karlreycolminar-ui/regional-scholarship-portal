from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import AuditLog


@login_required
def audit_log_view(request):
    if not request.user.is_admin:
        return HttpResponseForbidden('Access denied.')
    logs = AuditLog.objects.select_related('user').all()
    action_filter = request.GET.get('action', '')
    user_filter = request.GET.get('user', '')
    if action_filter:
        logs = logs.filter(action_type=action_filter)
    if user_filter:
        logs = logs.filter(user__username__icontains=user_filter)
    return render(request, 'audits/logs.html', {
        'logs': logs[:200],
        'action_filter': action_filter,
        'user_filter': user_filter,
        'action_choices': AuditLog.ACTION_CHOICES,
    })

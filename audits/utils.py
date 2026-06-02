from .models import AuditLog


def log_action(user, action_type, description, request=None):
    """
    Helper to create an audit log entry.
    Usage: log_action(request.user, 'APPLICATION_SUBMITTED', 'Applied for XYZ')
    """
    ip = None
    if request:
        x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded:
            ip = x_forwarded.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
    AuditLog.objects.create(
        user=user,
        action_type=action_type,
        description=description,
        ip_address=ip
    )

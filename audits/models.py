from django.db import models
from django.conf import settings


class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('USER_REGISTERED', 'User Registered'),
        ('USER_LOGIN', 'User Login'),
        ('USER_LOGOUT', 'User Logout'),
        ('USER_EDITED', 'User Edited'),
        ('USER_STATUS_CHANGED', 'User Status Changed'),
        ('PROFILE_UPDATED', 'Profile Updated'),
        ('PASSWORD_CHANGED', 'Password Changed'),
        ('APPLICATION_SUBMITTED', 'Application Submitted'),
        ('APPLICATION_REVIEWED', 'Application Reviewed'),
        ('APPLICATION_WITHDRAWN', 'Application Withdrawn'),
        ('SCHOLARSHIP_CREATED', 'Scholarship Created'),
        ('SCHOLARSHIP_UPDATED', 'Scholarship Updated'),
        ('SCHOLARSHIP_DELETED', 'Scholarship Deleted'),
        ('DOCUMENT_UPLOADED', 'Document Uploaded'),
        ('API_REGISTER', 'API Register'),
        ('API_LOGIN', 'API Login'),
        ('API_LOGOUT', 'API Logout'),
        ('API_APPLICATION_SUBMITTED', 'API Application Submitted'),
        ('API_APPLICATION_REVIEWED', 'API Application Reviewed'),
        ('API_APPLICATION_WITHDRAWN', 'API Application Withdrawn'),
        ('API_SCHOLARSHIP_CREATED', 'API Scholarship Created'),
        ('API_SCHOLARSHIP_UPDATED', 'API Scholarship Updated'),
        ('API_SCHOLARSHIP_DELETED', 'API Scholarship Deleted'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, related_name='audit_logs'
    )
    action_type = models.CharField(max_length=50, choices=ACTION_CHOICES)
    description = models.TextField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Audit Log'
        verbose_name_plural = 'Audit Logs'

    def __str__(self):
        user_str = self.user.username if self.user else 'System'
        return f"[{self.timestamp:%Y-%m-%d %H:%M}] {user_str} - {self.action_type}"

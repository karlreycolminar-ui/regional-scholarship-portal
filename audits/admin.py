from django.contrib import admin
from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'user', 'action_type', 'description', 'ip_address']
    list_filter = ['action_type']
    search_fields = ['user__username', 'description']
    readonly_fields = ['user', 'action_type', 'description', 'ip_address', 'timestamp']
    ordering = ['-timestamp']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

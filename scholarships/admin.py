from django.contrib import admin
from .models import Scholarship

@admin.register(Scholarship)
class ScholarshipAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'amount', 'slots', 'deadline', 'is_active', 'created_by']
    list_filter = ['category', 'is_active']
    search_fields = ['title', 'description']
    ordering = ['-created_at']

from django.contrib import admin
from .models import Application, Document


class DocumentInline(admin.TabularInline):
    model = Document
    extra = 0
    readonly_fields = ['uploaded_at']


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'scholarship', 'status', 'date_submitted', 'reviewed_by']
    list_filter = ['status', 'scholarship']
    search_fields = ['user__username', 'user__email', 'scholarship__title']
    ordering = ['-date_submitted']
    readonly_fields = ['date_submitted', 'updated_at']
    inlines = [DocumentInline]


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['application', 'file_type', 'original_filename', 'uploaded_at']
    list_filter = ['file_type']

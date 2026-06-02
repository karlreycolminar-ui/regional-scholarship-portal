from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse


def health_check(request):
    return JsonResponse({
        'status': 'ok',
        'version': settings.APP_VERSION,
        'debug': settings.DEBUG,
        'axes_enabled': getattr(settings, 'AXES_ENABLED', False),
    })

urlpatterns = [
    path('healthz/', health_check, name='health_check'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('scholarships/', include('scholarships.urls')),
    path('applications/', include('applications.urls')),
    path('audits/', include('audits.urls')),
    path('', include('accounts.urls_dashboard')),
    path('api/', include('accounts.api_urls')),
    path('api/', include('scholarships.api_urls')),
    path('api/', include('applications.api_urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

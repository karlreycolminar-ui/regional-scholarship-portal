from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
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

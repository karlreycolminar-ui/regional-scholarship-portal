from django.urls import path
from .api_views import (
    ApplicationListCreateAPIView, ApplicationDetailAPIView,
    ReviewDecisionAPIView, DocumentUploadAPIView, AdminApplicationListAPIView
)

urlpatterns = [
    path('applications/', ApplicationListCreateAPIView.as_view(), name='api_applications'),
    path('applications/<int:pk>/', ApplicationDetailAPIView.as_view(), name='api_application_detail'),
    path('applications/<int:pk>/review/', ReviewDecisionAPIView.as_view(), name='api_review_decision'),
    path('applications/<int:pk>/documents/', DocumentUploadAPIView.as_view(), name='api_document_upload'),
    path('admin/applications/', AdminApplicationListAPIView.as_view(), name='api_admin_applications'),
]

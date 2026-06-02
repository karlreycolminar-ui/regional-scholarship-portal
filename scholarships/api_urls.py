from django.urls import path
from .api_views import (
    ScholarshipListAPIView, ScholarshipDetailAPIView,
    ScholarshipCreateAPIView, ScholarshipUpdateAPIView
)

urlpatterns = [
    path('scholarships/', ScholarshipListAPIView.as_view(), name='api_scholarship_list'),
    path('scholarships/create/', ScholarshipCreateAPIView.as_view(), name='api_scholarship_create'),
    path('scholarships/<int:pk>/', ScholarshipDetailAPIView.as_view(), name='api_scholarship_detail'),
    path('scholarships/<int:pk>/manage/', ScholarshipUpdateAPIView.as_view(), name='api_scholarship_manage'),
]

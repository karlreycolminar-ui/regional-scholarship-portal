from django.urls import path
from . import views

urlpatterns = [
    path('apply/<int:scholarship_id>/', views.apply_view, name='apply'),
    path('my/', views.my_applications, name='my_applications'),
    path('<int:pk>/', views.application_detail, name='application_detail'),
    path('<int:pk>/withdraw/', views.application_withdraw, name='application_withdraw'),
    path('review/', views.review_list, name='review_list'),
    path('review/<int:pk>/', views.review_application, name='review_application'),
]

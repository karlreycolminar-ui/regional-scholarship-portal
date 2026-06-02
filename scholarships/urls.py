from django.urls import path
from . import views

urlpatterns = [
    path('', views.scholarship_list, name='scholarship_list'),
    path('<int:pk>/', views.scholarship_detail, name='scholarship_detail'),
    path('create/', views.scholarship_create, name='scholarship_create'),
    path('<int:pk>/edit/', views.scholarship_edit, name='scholarship_edit'),
    path('<int:pk>/delete/', views.scholarship_delete, name='scholarship_delete'),
]

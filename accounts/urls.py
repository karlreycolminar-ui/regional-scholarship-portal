from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('manage-users/', views.manage_users_view, name='manage_users'),
    path('manage-users/<int:user_id>/edit/', views.edit_user_view, name='edit_user'),
    path('manage-users/<int:user_id>/toggle/', views.toggle_user_active, name='toggle_user_active'),
]

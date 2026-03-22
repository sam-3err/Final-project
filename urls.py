from django.urls import path
from .views import register, login, profile, get_users  # Add get_users import
from . import views
urlpatterns = [
    path('register/', register),
    path('login/', login),
    path('profile/', profile),
      path('delete/<int:id>/', views.delete_user),
    path('users/', get_users),  # NEW: List all users for Admin dashboard
]

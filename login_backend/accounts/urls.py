# accounts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_user, name='register'),
    path('password_reset/', views.register_user, name='password_reset'),
    path('api/add-users/', views.add_users),
]

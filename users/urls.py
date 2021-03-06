from django.urls import path
from . import views

urlpatterns = [
    path('', views.profiles, name='profiles'),
    path('profile/<str:pk>/', views.user_profile, name="user-profile"),

    path('login/', views.login_user, name='login'),
    path('register/', views.register_user, name='register'),
    path('logout/', views.logout_user, name='logout'),
]
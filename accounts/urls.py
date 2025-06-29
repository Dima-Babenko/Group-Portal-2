from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/edit-profile/', views.edit_profile_view, name='edit-profile'),
    path('profile/<str:username>/', views.user_profile_view, name='user-profile'),
    path('', views.home_view, name='home'),
]



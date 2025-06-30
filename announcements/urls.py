from django.urls import path
from . import views

app_name = 'announcements'

urlpatterns = [
    path('', views.announcement_list, name='announcement_list'),
    path('create/', views.announcement_create, name='announcement_create'),
    path('<int:pk>/update/', views.announcement_update, name='announcement_edit'),
    path('<int:pk>/delete/', views.announcement_delete, name='announcement_delete'),
]

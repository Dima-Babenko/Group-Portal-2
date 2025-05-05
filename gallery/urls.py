from django.urls import path
from . import views

app_name = 'gallery'

urlpatterns = [
    path('', views.gallery_view, name='gallery_view'),
    path('add/', views.add_media, name='add_media'),
    path('edit/<int:pk>/', views.edit_media, name='edit_media'),
    path('delete/<int:pk>/', views.delete_media, name='delete_media'),
]

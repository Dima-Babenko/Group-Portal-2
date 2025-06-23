from django.urls import path
from . import views

app_name = 'diary'

urlpatterns = [
    path('schedule-with-grades/', views.get_schedule_with_grades, name='schedule_with_grades'),
]
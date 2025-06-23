from django.urls import path
from . import views

app_name = 'polls'

urlpatterns = [
    path('poll_list/', views.PollListView.as_view(), name='poll_list'),
    path('create/', views.PollCreateView.as_view(), name='poll_create'),
    path('<int:poll_id>/add_question/', views.AddQuestionView.as_view(), name='add_question'),
    path('<int:question_id>/add_option/', views.AddOptionView.as_view(), name='add_option'),
    path('detail/<int:pk>/', views.PollDetailView.as_view(), name='poll_detail'),
    path('results/<int:pk>/', views.PollResultsView.as_view(), name='poll_results'),  # <-- оце обов'язково
]
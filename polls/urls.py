from django.urls import path
from polls import views

app_name = "polls"

urlpatterns = [
    path('poll_list', views.PollListView.as_view(), name="poll_list"),
]
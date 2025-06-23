from django.urls import path
from . import views

app_name = 'voting'

urlpatterns = [
    path('voting_list/', views.voting_list, name='voting_list'),
    path('<int:voting_id>/', views.voting_detail, name='voting_detail'),
    path('<int:voting_id>/results/', views.voting_results, name='voting_results'),
    path('create_voting/', views.create_voting, name='create_voting'),
    path('<int:pk>/delete/', views.delete_voting, name='delete_voting'),
]

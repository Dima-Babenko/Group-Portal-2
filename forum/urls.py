from django.urls import path, include
from forum import views

app_name = "forum"

urlpatterns = [
    path('branch_list', views.BranchListView.as_view(), name="branch_list"),
    path('<int:pk>/', views.BranchDetailView.as_view(), name="branch_detail"),
    path('<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('branch_create', views.BranchCreateView.as_view(), name="branch_create"),
    path('<int:pk>/update/', views.BranchUpdateView.as_view(), name="branch_update"),
    path('<int:pk>/delete/', views.BranchDeleteView.as_view(), name="branch_delete"),
    path('comment/delete/<int:pk>/', views.CommentDeleteView.as_view(), name='comment_delete'),
]
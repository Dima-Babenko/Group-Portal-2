from django.urls import path, include
from portfolio import views

app_name = 'portfolio'

urlpatterns = [
    path('project_list/', views.PortfolioListView.as_view(), name="project_list"),
    path('project_create/', views.PortfolioCreateView.as_view(), name="project_create"),
    path('<int:pk>/update/', views.PortfolioUpdateView.as_view(), name="project_update"),
    path('<int:pk>/delete/', views.PortfolioDeleteView.as_view(), name="project_delete"),
    path('project/<int:pk>/like/', views.PortfolioLikeView.as_view(), name="project_like"),
    path('project/<int:pk>/dislike/', views.PortfolioDisLikeView.as_view(), name="project_dislike"),
]
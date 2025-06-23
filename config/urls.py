from django.contrib import admin
from django.urls import path, include
from accounts import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('voting/', include('voting.urls')),
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', views.home_view, name='home'),
    path('', include('forum.urls', namespace='forum')),
    path('portfolio/', include('portfolio.urls')),
    path('diary/', include('diary.urls', namespace='diary')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

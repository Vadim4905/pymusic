from django.urls import path
from . import views





urlpatterns = [
    path('scrape/artist', views.ArtistScrapeCreateView.as_view(), name='scrape-artist'),
    path('download-progress/<str:task_id>/', views.download_progress, name='download-progress'),
    path('task-status/<str:task_id>/', views.task_status, name='task-status'),
    path('progress', views.start_task, name='start_task'),


]
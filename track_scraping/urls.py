from django.urls import path
from . import views





urlpatterns = [
    path('scrape/artist', views.ArtistScrapeCreateView.as_view(), name='scrape_artist'),
    path('download_progress/<str:task_id>/', views.download_progress, name='download_progress'),
    path('task_status/<str:task_id>/', views.task_status, name='task_status'),
    path('progress', views.start_task, name='start_task'),


]
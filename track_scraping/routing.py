from django.urls import re_path
from track_scraping.consumers import ProgressBarConsumer

websocket_urlpatterns = [
    re_path(r'ws/progress_bar/(?P<task_id>[0-9a-fA-F-]{36})/$', ProgressBarConsumer.as_asgi()),  
]
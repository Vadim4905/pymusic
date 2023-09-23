from django.urls import path
from . import views





urlpatterns = [
    path('scrape/artist',  views.ArtistScrapeCreateView.as_view(), name='scrape_artist'),
]
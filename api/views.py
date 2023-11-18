from django.shortcuts import render

# Create your views here.

from rest_framework import generics

from home import models
from rest_framework.views import APIView
from .serializers import MusicSerializer,PlaylistSerializer
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status


class MusicView(generics.ListCreateAPIView):
    serializer_class = MusicSerializer
    queryset = models.Music.objects.all()[:10]

class MusicDetailView(generics.RetrieveAPIView):
    queryset = models.Music.objects.all()
    serializer_class = MusicSerializer

class UserPlaylistsView(APIView):
    def get(self, request,  format=None):
        playlists = models.Playlist.objects.filter(user=self.request.user)
        print(playlists)
        serializer = PlaylistSerializer(playlists, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
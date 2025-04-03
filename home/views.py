from django.shortcuts import redirect,get_object_or_404
from django.views.generic import ListView, CreateView,DetailView
from django.views import View
from django.urls import reverse
from django.http import HttpResponseRedirect,HttpResponse,Http404
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

import os
import shutil
import tempfile
from zipfile import ZipFile

from home import models,forms
from .mixins import PlaylistContextFormMixin,GroupRequiredMixin


 
class MusicListView(PlaylistContextFormMixin,ListView):
    template_name = "home/index.html"
    model = models.Music
    context_object_name = "musics"
    queryset = models.Music.objects.all()[:10]
    
    def get_context_data(self, *args, **kwargs):
        return super().get_context_data(*args, **kwargs)



class ArtistCreateView(PlaylistContextFormMixin,GroupRequiredMixin,CreateView):
    template_name = "home/artist_create.html"
    form_class = forms.ArtistForm
    group_required = 'admin'

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER', ''))


class MusicCreateView(PlaylistContextFormMixin,GroupRequiredMixin,CreateView):
    template_name = "home/music_create.html"
    form_class = forms.MusicForm
    group_required = 'admin'

    def form_valid(self, form):
        album_id = self.kwargs.get('pk')
        music = form.save(commit=False)
        music.album = get_object_or_404(models.Album, pk=album_id)
        music.artist = music.album.artist
        music.save()
        url = reverse('album-detail',kwargs={'pk': album_id})
        return redirect(url)
    

class AlbumCreateView(PlaylistContextFormMixin,GroupRequiredMixin,CreateView):
    template_name = "home/album_create.html"
    form_class = forms.AlbumForm
    group_required = 'admin'

    def form_valid(self, form):
        artist_id = self.kwargs.get('pk')
        album = form.save(commit=False)
        album.artist = get_object_or_404(models.Artist, pk=artist_id)
        album.save()
        url = reverse('artist-detail',kwargs={'pk': artist_id})
        return redirect(url)


class ArtistsListView(PlaylistContextFormMixin,ListView):
    template_name = "home/artists_list.html"
    model = models.Artist
    context_object_name = "artists"

class ArtistDetailView(PlaylistContextFormMixin,DetailView):
    template_name = "home/artist_view.html"
    model = models.Artist
    context_object_name = "artist"

class AlbumDetailView(PlaylistContextFormMixin,DetailView):
    template_name = "home/album_view.html"
    model = models.Album
    context_object_name = "album"

class MusicDetailView(PlaylistContextFormMixin,DetailView):
    template_name = "home/music_view.html"
    model = models.Music
    context_object_name = "music"

class PlaylistCreateView(PlaylistContextFormMixin,LoginRequiredMixin,CreateView):
    template_name = "home/playlist_create.html"
    form_class = forms.PLaylistForm

    def form_valid(self, form):
        playlist = form.save(commit=False)
        playlist.user = self.request.user
        playlist.save()
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER', ''))

@login_required
def add_music_to_playlist(request, music_id, playlist_id):
    music = get_object_or_404(models.Music, pk=music_id)
    playlist = get_object_or_404(models.Playlist, pk=playlist_id)

    # Add music to playlist
    if playlist.user == request.user:
        playlist.musics.add(music)
        messages.success(request, f'Added {music.name} to {playlist.name}!')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', ''))

@login_required    
def remove_music_from_playlist(request, music_id, playlist_id):
    music = get_object_or_404(models.Music, pk=music_id)
    playlist = get_object_or_404(models.Playlist, pk=playlist_id)

    # Remove music from playlist
    if playlist.user == request.user:
        playlist.musics.remove(music)
        messages.success(request, f'Removed {music.name} from {playlist.name}!')
        
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', ''))

class PlaylistDetailView(PlaylistContextFormMixin,DetailView):
    template_name = "home/playlist_view.html"
    model = models.Playlist
    context_object_name = "playlist"

class SearchResultsListView(PlaylistContextFormMixin,ListView): 
    model = models.Music
    context_object_name = 'musics'
    template_name = 'home/search_results.html'

    def get_queryset(self): 
        query = self.request.GET.get('q')
        return models.Music.objects.filter(Q(name__icontains=query) | Q(name__icontains=query))

class BaseArchiveDownloadView(View):

    def get(self, request, *args, **kwargs):
        if self.kwargs.get('model_name') =='artist':
            artist =  get_object_or_404(models.Artist, pk=self.kwargs.get('model_id'))
            return self.create_archive(artist.musics.all(),artist.name)
        elif self.kwargs.get('model_name') =='album':
            album =  get_object_or_404(models.Album, pk=self.kwargs.get('model_id'))
            return self.create_archive(album.musics.all(),album.name)
        elif self.kwargs.get('model_name') =='playlist':
            playlist =  get_object_or_404(models.Playlist, pk=self.kwargs.get('model_id'))
            return self.create_archive(playlist.musics.all(),playlist.name)
        else:
            raise Http404()

    def clear_filename(self,filename,forbited_punct='\/:?*<>|"',replce_to='-'):
        for punct in forbited_punct:
            filename = filename.replace(punct,replce_to)
        return filename

    def create_archive(self,models,archive_name):
        temp_dir = tempfile.mkdtemp()
        archive_name = self.clear_filename(archive_name)

        zip_filename = f"{archive_name}.zip"
        zip_filepath = os.path.join(temp_dir, zip_filename)

        with ZipFile(zip_filepath, 'w') as zipf:
            for file_model in models:
                artist_name = self.clear_filename(file_model.artist.name)
                album_name = self.clear_filename(file_model.album.name)
                music_name = self.clear_filename(file_model.name)+'.mp3'
                zip_path = os.path.join(artist_name,album_name,music_name)
                zipf.write(file_model.track.path,zip_path)

        response = HttpResponse(content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename="{zip_filename}"'

        with open(zip_filepath, 'rb') as zip_file:
            response.write(zip_file.read())

        shutil.rmtree(temp_dir)
        return response



from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import ListView, CreateView,DetailView
from django.views import View
from django.urls import reverse
from django.http import HttpResponseRedirect,HttpResponse,Http404,HttpResponseBadRequest
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
# from braces.views import GroupRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
import shutil
import tempfile
from zipfile import ZipFile

from home import models,forms

class GroupRequiredMixin(UserPassesTestMixin):
    group_required = None  # List of group names

    def test_func(self):
        if not self.request.user.is_authenticated:
            return False

        if self.group_required is None:
            return True

        if isinstance(self.group_required, str):
            groups = [self.group_required]
        else:
            groups = self.group_required

        return self.request.user.groups.filter(name__in=groups).exists() or self.request.user.is_superuser


 
 
class IndexView(ListView):
    template_name = "home/index.html"
    model = models.Music
    context_object_name = "musics"
    queryset = models.Music.objects.all()[:10]

    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(**kwargs)
        context['musics_json'] = serialize('json', models.Music.objects.all())
        context['title'] = 'Index'
        context['form'] = forms.PLaylistForm
        if self.request.user.is_authenticated:
            context['user_playlists'] = models.Playlist.objects.filter(user=self.request.user)
        return context

# admin_requred
class ArtistCreateView(GroupRequiredMixin,CreateView):
    template_name = "home/artist_create.html"
    form_class = forms.ArtistForm
    group_required = 'admin'

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER', '/default/url/'))

# admin_requred
class MusicCreateView(GroupRequiredMixin,CreateView):
    template_name = "home/music_create.html"
    form_class = forms.MusicForm
    group_required = 'admin'

    def form_valid(self, form):
        album_id = self.kwargs.get('pk')
        music = form.save(commit=False)
        music.album = get_object_or_404(models.Album, pk=album_id)
        music.artist = music.album.artist
        music.save()
        url = reverse('album_detail',kwargs={'pk': album_id})
        return redirect(url)
# admin_requred

class AlbumCreateView(GroupRequiredMixin,CreateView):
    template_name = "home/album_create.html"
    form_class = forms.AlbumForm
    group_required = 'admin'

    def form_valid(self, form):
        artist_id = self.kwargs.get('pk')
        album = form.save(commit=False)
        album.artist = get_object_or_404(models.Artist, pk=artist_id)
        album.save()
        url = reverse('artist_detail',kwargs={'pk': artist_id})
        return redirect(url)


class ArtistsList(ListView):
    template_name = "home/artists_list.html"
    model = models.Artist
    context_object_name = "artists"

class ArtistView(DetailView):
    template_name = "home/artist_view.html"
    model = models.Artist
    context_object_name = "artist"

    def get_context_data(self,*args,object_list=None,**kwargs):

        context = super().get_context_data(**kwargs)
        context['title'] = 'Artist'
        # category = context['category']
        # products = Product.objects.filter(category=category)
        # context['products'] = products
        context['albums'] = models.Album.objects.filter(artist=kwargs['object'])
        # context['categories'] = Category.objects.all()
        return context

class AlbumView(DetailView):
    template_name = "home/album_view.html"
    model = models.Album
    context_object_name = "album"

    def get_context_data(self,*args,object_list=None,**kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Album'
        if self.request.user.is_authenticated:
            context['user_playlists'] = models.Playlist.objects.filter(user=self.request.user)
        context['musics'] = models.Music.objects.filter(album=kwargs['object'])
        # context['categories'] = Category.objects.all()
        return context

class MusicView(DetailView):
    template_name = "home/music_view.html"
    model = models.Music
    context_object_name = "music"

#login_requred
class PlaylistCreateView(LoginRequiredMixin,CreateView):
    template_name = "home/playlist_create.html"
    form_class = forms.PLaylistForm


    def form_valid(self, form):
        playlist = form.save(commit=False)
        playlist.user = self.request.user
        playlist.save()
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER', '/default/url/'))

@login_required
def add_music_to_playlist(request, music_id, playlist_id):
    music = get_object_or_404(models.Music, pk=music_id)
    playlist = get_object_or_404(models.Playlist, pk=playlist_id)

    # Add music to playlist
    if playlist.user == request.user:
        playlist.musics.add(music)
        messages.success(request, f'Added {music.name} to {playlist.name}!')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/default/url/'))

@login_required    
def remove_music_from_playlist(request, music_id, playlist_id):
    music = get_object_or_404(models.Music, pk=music_id)
    playlist = get_object_or_404(models.Playlist, pk=playlist_id)

    # Remove music from playlist
    if playlist.user == request.user:
        playlist.musics.remove(music)
        messages.success(request, f'Removed {music.name} from {playlist.name}!')
        
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/default/url/'))

class PlaylistView(DetailView):
    template_name = "home/playlist_view.html"
    model = models.Playlist
    context_object_name = "playlist"

class SearchResultsListView(ListView): 
    model = models.Music
    context_object_name = 'musics'
    template_name = 'home/search_results.html'

    def get_queryset(self): 
        query = self.request.GET.get('q')
        return models.Music.objects.filter(Q(name__icontains=query) | Q(name__icontains=query))

class BaseArchiveDownloadView(View):
    model_downlod_from = None

    def get(self, request, model_id, *args, **kwargs):
        # Get all FileModel instances
        requsted_model = get_object_or_404(self.model_downlod_from, pk=model_id)
        if isinstance(requsted_model, models.Album):
            file_models =  models.Music.objects.filter(album=requsted_model)
        elif isinstance(requsted_model,  models.Artist):
            file_models =  models.Music.objects.filter(artist=requsted_model)
        elif isinstance(requsted_model,  models.Playlist):
            file_models =  requsted_model.musics.all()

        return self.create_archive(file_models,requsted_model.name)

    def create_archive(self,models,archive_name):
        temp_dir = tempfile.mkdtemp()

        # Iterate through each instance, copy its file to the temp directory
        # for file_model in models:
        #     source_file_path = file_model.track.path
        #     destination_file_path = os.path.join(temp_dir, os.path.basename(source_file_path))
        #     shutil.copy2(source_file_path, destination_file_path)

        # Create a zip archive
        zip_filename = f"{archive_name}.zip"
        zip_filepath = os.path.join(temp_dir, zip_filename)

        with ZipFile(zip_filepath, 'w') as zipf:
            # for root, _, files in os.walk(temp_dir):
            #     for file in files:
            #         file_path = os.path.join(root, file)
            #         zipf.write(file_path, os.path.relpath(file_path, temp_dir))
            for file_model in models:
                print(file_model.track.path)
                zipf.write(file_model.track.path,f'{file_model.name}.mp3')

        # Create a response with the zip file
        response = HttpResponse(content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename="{zip_filename}"'

        with open(zip_filepath, 'rb') as zip_file:
            response.write(zip_file.read())

        # Clean up the temporary directory
        shutil.rmtree(temp_dir)

        return response

class ArchiveDownloadAlbumView(BaseArchiveDownloadView):
    model_downlod_from = models.Album

class ArchiveDownloadArtistView(BaseArchiveDownloadView):
    model_downlod_from = models.Artist

class ArchiveDownloadPlaylistView(BaseArchiveDownloadView):
    model_downlod_from = models.Playlist
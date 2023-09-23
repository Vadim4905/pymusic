from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import ListView, CreateView,DetailView
from home import models,forms
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
# from braces.views import GroupRequiredMixin
from django.contrib.auth.decorators import login_required

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

    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(**kwargs)
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
    playlist.musics.add(music)

    messages.success(request, f'Added {music.name} to {playlist.name}!')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/default/url/'))

@login_required    
def remove_music_from_playlist(request, music_id, playlist_id):
    music = get_object_or_404(models.Music, pk=music_id)
    playlist = get_object_or_404(models.Playlist, pk=playlist_id)

    # Remove music from playlist
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
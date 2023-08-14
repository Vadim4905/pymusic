from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import ListView, CreateView,DetailView
from home import models,forms
from django.urls import reverse
from django.http import HttpResponseRedirect
# Create your views here.

class IndexView(ListView):
    template_name = "home/index.html"
    model = models.Music
    context_object_name = "musics"

    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(**kwargs)
        # context['title'] = 'Artist'
        # # category = context['category']
        # # products = Product.objects.filter(category=category)
        # # context['products'] = products
        # context['albums'] = models.Album.objects.filter(artist=kwargs['object'])
        # # context['categories'] = Category.objects.all()
        return context


class ArtistCreateView(CreateView):
    template_name = "home/artist_create.html"
    form_class = forms.ArtistForm

    def form_valid(self, form):
        form.save()
        return redirect(to="/")

class MusicCreateView(CreateView):
    template_name = "home/music_create.html"
    form_class = forms.MusicForm

    def form_valid(self, form):
        album_id = self.kwargs.get('pk')
        music = form.save(commit=False)
        music.album = get_object_or_404(models.Album, pk=album_id)
        music.artist = music.album.artist
        music.save()
        url = reverse('album_detail',kwargs={'pk': album_id})
        return redirect(url)

class AlbumCreateView(CreateView):
    template_name = "home/album_create.html"
    form_class = forms.AlbumForm

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
        # category = context['category']
        # products = Product.objects.filter(category=category)
        # context['products'] = products
        context['musics'] = models.Music.objects.filter(album=kwargs['object'])
        # context['categories'] = Category.objects.all()
        return context

class PlaylistCreateView(CreateView):
    template_name = "home/playlist_create.html"
    form_class = forms.PLaylistForm

    def form_valid(self, form):
        playlist = form.save(commit=False)
        playlist.user = self.request.user
        playlist.save()
        return redirect(to="/")

def add_music_to_playlist(request, music_id, playlist_id):
    music = get_object_or_404(models.Music, pk=music_id)
    playlist = get_object_or_404(models.Playlist, pk=playlist_id)

    # Add music to playlist
    playlist.musics.add(music)

    messages.success(request, f'Added {music.name} to {playlist.name}!')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/default/url/'))
from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import ListView, CreateView,DetailView,FormView 
from track_scraping import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin

from home.models import Artist,Album,Music
from home.views import GroupRequiredMixin
from track_scraping.artist_scrape import scrape_artist

from ytmusicapi import YTMusic
import asyncio
import aiohttp
import aiofiles
import json
from asgiref.sync import sync_to_async
from django.core.files import File
from datetime import date
from pytube import YouTube

from concurrent.futures import ThreadPoolExecutor
import time
import os
import yt_dlp as ydlp



class ArtistScrapeCreateView(GroupRequiredMixin,FormView ):
    template_name = "track_scraping/scrape_artist.html"
    form_class = forms.ArtistForm
    group_required = 'admin'

    async def fetch_track(self,url, artist_model,album_model, track_name):

        yt = YouTube(url)
        stream = yt.streams.filter(only_audio=True).first()
        file_path = stream.download()  # Скачивание файла

        with open(file_path,'rb') as f:
            music_model = Music(name=track_name,artist=artist_model,album=album_model,created=date.today(),track=File(f,name='track.mp3'))
            await self.save_model(music_model)
        # os.remove(file_path)
    
    @sync_to_async
    def save_model_async(self,model):
        model.save()

    def download_track(self,url, artist_model,album_model, track_name):
        options = {
                    'format': 'bestaudio/best',
                    'outtmpl': f'tracks/%(title)s.%(ext)s',  # путь для сохранения
                    'extractaudio': True,
                    'audioformat': 'mp3',
                    # 'progress_hooks': [my_hook],
                }
        with ydlp.YoutubeDL(options) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            video_title = info_dict.get('title', None)
            ext =  info_dict.get('ext', None)
            filename = ydl.prepare_filename(info_dict)

        with open(filename,'rb') as f:
            music_model = Music(name=track_name,artist=artist_model,album=album_model,created=date.today(),track=File(f,name='track.mp3'))
            music_model.save()

    def execute_tasks(self,task_args,max_workers=25):
        retry_list = []
        with ThreadPoolExecutor(max_workers=25) as executor:
            futures = {executor.submit(self.download_track, *args): args for args in task_args}
            for future in futures:
                initial_args = futures[future]
                try:
                    future.result()
                except Exception as e:
                    print(e)
                    # time.sleep(5)
                    # Modify the arguments for retry. In this case, I'm modifying the 'modifier' argument.
                    retry_list.append(initial_args)
            if retry_list:
                print("Retrying failed tasks...")
                self.execute_tasks(retry_list)

    
    async def scrape_artist(self,artist_name):
        async with aiohttp.ClientSession() as session:
            ytmusic = YTMusic()  
            search_results = ytmusic.search(artist_name, filter='artists')

            if not search_results:
                return

            artist = ytmusic.get_artist(search_results[0]['browseId'])
            artist_name = artist['name']
            artist_albums = artist['albums']
            artist_photo_url = artist['thumbnails'][0]['url']

            response = await session.get(url=artist_photo_url)
            async with aiofiles.open('photo.jpg', 'wb') as f:
                await f.write(await response.read())

            with open('photo.jpg','rb') as f:
                artist_model = Artist(name=artist_name,photo=File(f,name='photo.jpg'))
                await self.save_model_async(artist_model)
            
            initial_tasks  = []
            for album in artist_albums['results']:
                album_photo_url = album['thumbnails'][0]['url']
                album_name = album['title']

                response = await session.get(url=album_photo_url)
                async with aiofiles.open('photo.jpg', 'wb') as f:
                    await f.write(await response.read())

                with open('photo.jpg','rb') as f:
                    album_model = Album(name=album_name,artist=artist_model,cover=File(f,name='photo.jpg'))
                    await self.save_model_async(album_model)

                tracks = ytmusic.get_album(album['browseId'])['tracks']
                for track in tracks:
                    video_id = track['videoId']
                    track_name = track['title']
                    video_url = f"https://www.youtube.com/watch?v={video_id}"
                    initial_tasks.append((video_url,artist_model,album_model, track_name))
            self.execute_tasks(initial_tasks)

            

    def form_valid(self, form):
        artist_name = form.cleaned_data['name']
        asyncio.run(self.scrape_artist(artist_name))

        url = reverse('artists_list')
        return redirect(url)

# def get_download_progress(request, artist_name):
    



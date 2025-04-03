from celery import shared_task
from celery.result import AsyncResult

from ytmusicapi import YTMusic
from home.models import Artist,Album,Music
from django.core.files import File
from channels.layers import get_channel_layer
import requests
from django.core.files.base import ContentFile

import yt_dlp as ydlp

from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor 
from time import sleep
import os
import asyncio
import tempfile
import shutil
from asgiref.sync import async_to_sync




def worker(self,video_url):
    options = {
            'format': 'bestaudio/best',
            'outtmpl':f'tracks/%(title)s.%(ext)s',  
            'extractaudio': True,
            'audioformat': 'mp3',
            # 'proxy': 'http://43.167.164.59:13001',
            # 'progress_hooks': [my_hook],
        }
    with ydlp.YoutubeDL(options) as ydl:
        info_dict = ydl.extract_info(video_url, download=True)
        video_title = info_dict.get('title', None)
        ext =  info_dict.get('ext', None)
        filename = ydl.prepare_filename(info_dict)


@shared_task(bind=True)
def my_long_task(self, total):

    # for i in range(total):
    #     sleep(0.1)
    #     self.update_state(state='PROGRESS', meta={'progress': 100 * i / total})


    ytmusic = YTMusic()  
    search_results = ytmusic.search('twenty one pilots', filter='artists')

    artist = ytmusic.get_artist(search_results[0]['browseId'])

    albums_id = artist['albums']['browseId']
    if albums_id is None:
        artist_albums = artist['albums']['results']
    else:
        params = artist['albums']['params']
        artist_albums = ytmusic.get_artist_albums(albums_id,params)


    urls = []

    artist_albums = [ytmusic.get_album(album['browseId']) for album in artist_albums]
    for album in artist_albums:
        tracks = album['tracks']
        for track in tracks:
            video_id = track['videoId']                 
            track_name = track['title']
            urls.append(f"https://www.youtube.com/watch?v={video_id}")    
            
    task_args = [(self,url) for url in urls]
    with ThreadPoolExecutor(max_workers=25) as executor:
        futures = {executor.submit(worker, *args): args for args in task_args}
        for index, future in enumerate(futures):
            initial_args = futures[future]
            try:
                future.result()
                # index += 1
                # result = self.AsyncResult(self.request.id)
                # result.backend.store_result(
                #     task_id=self.request.id,
                #     result={'progress':index},
                #     state='PROGRESS',
                # )
                self.update_state(state='PROGRESS', meta={'progress': 100 * index / len(futures)})
                print(index)
            except Exception as e:
                print(e)

 
    return 'Task completed'



def download_track(video_id, artist_model,album_model,track_name,ytmusic,save_path):
        options = {
                    'format': 'bestaudio/best',
                    'outtmpl': f'{save_path}/%(title)s.%(ext)s',  
                    'extractaudio': True,
                    'audioformat': 'mp3',
                    # 'progress_hooks': [my_hook],
                }

        video_url = f"https://www.youtube.com/watch?v={video_id}"                   
        viewCount = ytmusic.get_song(video_id)['videoDetails'].get('viewCount', 0)
        watch_data = ytmusic.get_watch_playlist(video_id)
        if watch_data['lyrics'] is None:
            lyrics =''
        else:
            lyrics = ytmusic.get_lyrics(watch_data['lyrics']) 

        with ydlp.YoutubeDL(options) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            video_title = info_dict.get('title', None)
            ext =  info_dict.get('ext', None)
            filename = ydl.prepare_filename(info_dict)

        with open(filename,'rb') as f:
            music_model = Music(
                        name=track_name,
                        artist=artist_model,
                        album=album_model,
                        track=File(f,name=f'{track_name}.mp3'),
                        viewCount=viewCount,
                        lyrics = lyrics,
                        )
            music_model.save()


        # self.update_state(state='PROGRESS', meta={'progress': progress}) #NOT NULL constraint failed: django_celery_results_taskresult.task_id error
        os.remove(filename)
        


def execute_tasks(self,task_args,max_workers=25,max_retries=3,current_retry=0):
    retry_list = []
    channel_layer = get_channel_layer()
    
    with ThreadPoolExecutor(max_workers=15) as executor:
        futures = {executor.submit(download_track, *args): args for args in task_args}
        for index, future in enumerate(futures):
            initial_args = futures[future]
            try:
                future.result()
                progress = 100 * (index) / len(futures)
                asyncio.run(channel_layer.group_send(
                        self.request.id,
                        {"state":'PROGRESS',"type": "send_progress", "progress": progress, 'info': f"{index} of {len(futures)} downloaded"}
                    ))
                # self.update_state(state='PROGRESS', meta={'progress':progress,'info':f'{index} of {len(futures)} downloaded' })
            except Exception as e:
                print(e)
                # time.sleep(5)
                # Modify the arguments for retry. In this case, I'm modifying the 'modifier' argument.
                # could be changed proxy 
                retry_list.append(initial_args)

        if current_retry < max_retries and retry_list:
            print(f"Retrying failed tasks attempt {current_retry+1}")
            execute_tasks(self,retry_list,current_retry=current_retry+1)
        elif retry_list: 
            return "Scraping was't done successfully"


@shared_task(bind=True)
def scrape_artist(self,artist_name):
    # channel_layer = get_channel_layer()
    # task_id = self.request.id
    # for i in range(1, 201):  # Simulating a long-running task
    #     sleep(0.1)  # Simulate CPU load
    #     asyncio.run(channel_layer.group_send(
    #         task_id,
    #         {"state":'PROGRESS',"type": "send_progress", "progress": i/200*100, 'info': f"{i} of 200 downloaded"}
    #     ))
    
        
    with requests.Session() as session:
        ytmusic = YTMusic()  
        search_results = ytmusic.search(artist_name, filter='artists')

        artist = ytmusic.get_artist(search_results[0]['browseId'])
        artist_name = artist['name']
        artist_description = artist['description']

        if artist['thumbnails']:
            artist_photo_url = artist['thumbnails'][0]['url']   
            photo = ContentFile(session.get(url=artist_photo_url).content)
        else:
            photo = None

        albums_id = artist['albums']['browseId']
        if albums_id is None:
            artist_albums = artist['albums']['results']
        else:
            params = artist['albums']['params']
            artist_albums = ytmusic.get_artist_albums(albums_id,params)

        artist_model = Artist(
                            name=artist_name,
                            photo=photo,
                            description=artist_description,
                            )
        artist_model.save()
        artist_model.photo.save(f"{artist_name}.jpg", photo, save=True)
        
        initial_tasks  = []

        save_path = tempfile.mkdtemp()
        artist_albums = [ytmusic.get_album(album['browseId']) for album in artist_albums]

        for album in artist_albums:

            album_photo_url = album['thumbnails'][len(album['thumbnails'])-1]['url']#get the highest resolution

            cover  = ContentFile(session.get(url=album_photo_url).content)
            
            description = album.get('description','')
            if not description:
                description = ""
            album_model = Album(
                                name=album['title'],
                                artist=artist_model,
                                cover=cover,
                                year=album['year'],
                                duration=album['duration'],
                                trackCount=album['trackCount'],
                                duration_seconds=album['duration_seconds'],
                                description=description,
                                )
            album_model.save()
            album_model.cover.save(f"{album['title']}.jpg", cover, save=True)

        
            tracks = album['tracks']
            for track in tracks:
                video_id = track['videoId']                 
                track_name = track['title']
                initial_tasks.append((video_id,artist_model,album_model, track_name,ytmusic,save_path))
        result = execute_tasks(self,initial_tasks)
        shutil.rmtree(save_path)
        
        channel_layer = get_channel_layer()
        asyncio.run(channel_layer.group_send(
            self.request.id,
            {"state":'SUCCESS',"type": "send_progress", "progress": 100, 'info': "downloaded"}
        ))
        
        if result is not None:
            return result
        return "Downloaded successfully"
        

 



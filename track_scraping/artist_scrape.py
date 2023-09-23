from ytmusicapi import YTMusic
import json
from pathlib import Path
from django.core.files import File
import asyncio 
import aiohttp
import threading
from pytube import YouTube
from concurrent.futures import ThreadPoolExecutor
import time
import os
import yt_dlp as ydlp

start = time.time()


# class ArtistScrapeCreateView(GroupRequiredMixin,FormView ):
#     template_name = "track_scraping/scrape_artist.html"
#     form_class = forms.ArtistForm
#     group_required = 'admin'

#     async def fetch_track(self,url, artist_model,album_model, track_name):

#         yt = YouTube(url)
#         stream = yt.streams.filter(only_audio=True).first()
#         file_path = stream.download()  # Скачивание файла

#         with open(file_path,'rb') as f:
#             music_model = Music(name=track_name,artist=artist_model,album=album_model,created=date.today(),track=File(f,name='track.mp3'))
#             await self.save_model(music_model)
#         # os.remove(file_path)



    
#     @sync_to_async
#     def save_model(self,model):
#         model.save()

    
#     async def scrape_artist(self,artist_name):
#         async with aiohttp.ClientSession() as session:
#             ytmusic = YTMusic()  
#             search_results = ytmusic.search(artist_name, filter='artists')

#             if not search_results:
#                 return

#             artist = ytmusic.get_artist(search_results[0]['browseId'])
#             artist_name = artist['name']
#             artist_albums = artist['albums']
#             artist_photo_url = artist['thumbnails'][0]['url']

#             response = await session.get(url=artist_photo_url)
#             async with aiofiles.open('photo.jpg', 'wb') as f:
#                 await f.write(await response.read())

#             with open('photo.jpg','rb') as f:
#                 artist_model = Artist(name=artist_name,photo=File(f,name='photo.jpg'))
#                 await self.save_model(artist_model)
            
#             tasks = []
#             for album in artist_albums['results']:
#                 album_photo_url = album['thumbnails'][0]['url']
#                 album_name = album['title']

#                 response = await session.get(url=album_photo_url)
#                 async with aiofiles.open('photo.jpg', 'wb') as f:
#                     await f.write(await response.read())

#                 with open('photo.jpg','rb') as f:
#                     album_model = Album(name=album_name,artist=artist_model,cover=File(f,name='photo.jpg'))
#                     await self.save_model(album_model)

#                 tracks = ytmusic.get_album(album['browseId'])['tracks']
#                 for track in tracks:
#                     video_id = track['videoId']
#                     track_name = track['title']
#                     video_url = f"https://www.youtube.com/watch?v={video_id}"
#                     tasks.append(self.fetch_track(video_url, artist_model,album_model, track_name))

#             await asyncio.gather(*tasks)
                


#     def form_valid(self, form):
#         artist_name = form.cleaned_data['name']
#         asyncio.run(self.scrape_artist(artist_name))

#         url = reverse('artists_list')
#         return redirect(url)

def scrape_artist(artist_name):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(main(artist_name))

async def main(artist_name):
    ytmusic = YTMusic()  
    search_results = ytmusic.search(artist_name, filter='artists')

    artist = ytmusic.get_artist(search_results[0]['browseId'])

    artist_albums = artist['albums']
    artist_photo = artist['thumbnails'][0]['url']
    print(artist_photo)
    

async def fetch_artist():
    pass



# Print the titles of the albums
# for album in artist_albums['results'][0:1]:

#     album_tracks = ytmusic.get_album(album['browseId'])

#     for track in album_tracks['tracks'][0:1]:
#         print("Track:", track['title'],track['videoId'])
#         track_details = ytmusic.get_song(track['videoId'])
        
#         # with open('result.json','w',encoding='utf-8') as file:
#         #     json.dump(track_details,file,indent=4,ensure_ascii=False)

files = []

def my_hook(d):
    if d['status'] == 'finished':
        files.append(d['filename'])


def download_track(url, artist_name, track_name):
    # yt = YouTube(url)
    # stream = yt.streams.filter(only_audio=True).first()
    # file_path = stream.download('tracks')  # Скачивание файла
    options = {
                'format': 'bestaudio/best',
                'outtmpl': f'tracks/%(title)s.%(ext)s',  # путь для сохранения
                'extractaudio': True,
                'audioformat': 'mp3',
                'progress_hooks': [my_hook],
                # 'postprocessors': [{
                #     'key': 'FFmpegExtractAudio',
                #     'preferredcodec': 'mp3',
                # }]
            }

    with ydlp.YoutubeDL(options) as ydl:
        ydl.download([url])

def execute_tasks(task_args,max_workers=25):
    retry_list = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(download_track, *args): args for args in task_args}
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
            execute_tasks(retry_list)

def main(artist_name):
    ytmusic = YTMusic()
    search_results = ytmusic.search(artist_name, filter="artists")

    if not search_results:
        return None

    artist = ytmusic.get_artist(search_results[0]['browseId'])
    artist_albums = artist['albums']

    initial_tasks  = []
    current =0
    for album in artist_albums['results']:
        # Получаем треки из каждого альбома
        tracks = ytmusic.get_album(album['browseId'])['tracks']

        for track in tracks:
            video_id = track['videoId']
            track_name = track['title']
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            initial_tasks.append((video_url,artist_name,track_name))
    print(len(initial_tasks))
    execute_tasks(initial_tasks)
    print('Deleting files')
    for file_path in files:
        os.remove(file_path)


if __name__ == '__main__':
    main('twenty one pilots')
    print(f'executed for {time.time()-start}')




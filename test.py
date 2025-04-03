# import os
# import shutil
# import tempfile
# from zipfile import ZipFile


# temp_dir = tempfile.mkdtemp()


# def get_all_file_paths(directory): 
  
#     # initializing empty file paths list 
#     file_paths = [] 
  
#     # crawling through directory and subdirectories 
#     for root, directories, files in os.walk(directory): 
#         # print(root)
#         for filename in files: 
#             # join the two strings in order to form the full filepath. 
#             filepath = os.path.join(root, filename) 
#             file_paths.append(filepath) 
  
#     # returning all file paths 
#     return file_paths

# zip_filename = "archive.zip"
# zip_filepath = os.path.join(temp_dir, zip_filename)

# file_paths = get_all_file_paths('users')
# print(file_paths)

# with ZipFile(zip_filename, 'w') as zipf:
#     for file in file_paths: 
#         filename = file.rsplit("\\",1)[1]
#         zipf.write(file,filename) 

# shutil.rmtree(temp_dir)



import yt_dlp as ydlp
import shutil
import os
from concurrent.futures import ThreadPoolExecutor
from time import sleep
from ytmusicapi import YTMusic
from time import time
from fp.fp import FreeProxy

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
for album in artist_albums[0:1]:
    tracks = album['tracks']
    for track in tracks:
        video_id = track['videoId']                 
        track_name = track['title']
        urls.append(f"https://www.youtube.com/watch?v={video_id}")
        
        







video_id = 'NsSw3av755Y'
video_url = f"https://www.youtube.com/watch?v={video_id}"  

# with ydlp.YoutubeDL(options) as ydl:
#     info_dict = ydl.extract_info(video_url, download=True)
#     video_title = info_dict.get('title', None)
#     ext =  info_dict.get('ext', None)
#     filename = ydl.prepare_filename(info_dict)


def worker(video_url):
    
    options = {
            'format': 'bestaudio/best',
            'outtmpl':f'tracks/%(title)s.%(ext)s',  
            'extractaudio': True,
            'audioformat': 'mp3',
            'proxy': 'http://13.59.156.167:3128',
            # 'progress_hooks': [my_hook],
        }
    with ydlp.YoutubeDL(options) as ydl:
        info_dict = ydl.extract_info(video_url, download=True)
        video_title = info_dict.get('title', None)
        ext =  info_dict.get('ext', None)
        filename = ydl.prepare_filename(info_dict)


task_args = [ (url,) for url in urls]
start = time()
# with ThreadPoolExecutor(max_workers=25) as executor:
#     futures = {executor.submit(worker, *args): args for args in task_args}
#     for index, future in enumerate(futures):
#         initial_args = futures[future]
#         try:
#             future.result()
#             # print(index)
#         except Exception as e:
#             print(e)

# print(FreeProxy().get())

import yt_dlp
# youtube:player_client=web
ydl_opts = {
    'nocheckcertificate': True,
    # 'extractor_args': {
    #     'youtube': {
    #         "player_client": "web"
    #     },
    # },
    # 'quiet': True,
    'proxy': 'http://181.30.67.132:3663',  
    'format': 'bestaudio/best',
    'outtmpl': 'audio.mp3',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

url = "https://www.youtube.com/watch?v=NsSw3av755Y"

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])



       
print(time()-start)
#900s for 10 workers
#900s for 25 workers


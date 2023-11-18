# #pytube
# from pytube import YouTube
# # yt = YouTube('https://www.youtube.com/watch?v=VQHTROo0S8E').streams.filter(only_audio=True).first().download()

# yt = YouTube('https://www.youtube.com/watch?v=_EVKy35L7MM')
# video_stream = yt.streams.get_highest_resolution()

# # Download video
# video_stream.download()

from ytmusicapi import YTMusic
import json

ytmusic = YTMusic()  


def retry_on_error(max_retries=3,till_done=False, delay=5, exceptions=(Exception,)):
    """
    Decorator to retry a function in case of specified exceptions.

    Parameters:
    - max_retries (int): The maximum number of retries before giving up.
    - delay (int): The number of seconds to wait between retries.
    - exceptions (tuple): A tuple of exception classes to catch.
    """
    def decorator(function):
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries or till_done:
                try:
                    return function(*args, **kwargs)
                except exceptions as e:
                    retries += 1
                    if retries < max_retries:
                        print(f"Error: {e}. Retrying in {delay} seconds...")
                        time.sleep(delay)
                    else:
                        print("Max retries reached. Exiting...")
                        raise
        return wrapper
    return decorator

def get_song_lyrics(track_name):
    search_results = ytmusic.search(track_name, filter="songs")
    
    if not search_results:
        print(f"No track found with the name: {track_name}")
        return None

    track_id = search_results[0]['videoId']    

    watch_data =  ytmusic.get_watch_playlist(track_id)
    with open('result.json','w',encoding='utf-8') as file:
        json.dump(watch_data,file,indent=4,ensure_ascii=False)

    if watch_data['lyrics'] is None:
        print(f"No lyrics found for this song: {track_name}")
        return None

    lyrics_data = ytmusic.get_lyrics(watch_data['lyrics'])

    return lyrics_data['lyrics']


def get_track_details(track_name):
    # Search for the track
    search_results = ytmusic.search(track_name, filter="songs")
    
    if not search_results:
        print(f"No track found with the name: {track_name}")
        return None

    track_id = search_results[0]['videoId']

    # Get track details
    track_details = ytmusic.get_song(track_id)

    with open('result.json','w',encoding='utf-8') as file:
        json.dump(track_details,file,indent=4,ensure_ascii=False)
    
    # If the view count was provided by the API (this might not be the case):
    views = track_details['videoDetails'].get('viewCount', 0)
    return views


def get_artist_albums(artist_name):
    # Search for the artist
    search_results = ytmusic.search(artist_name, filter="artists")
    
    if not search_results:
        print(f"No artist found with the name: {artist_name}")
        return []

    artist_id = search_results[0]['browseId']
    artist = ytmusic.get_artist(artist_id)
    albums_id = artist['albums']['browseId']
    if albums_id is None:
        albums = artist['albums']['results']
    else:
        params = artist['albums']['params']
        albums = ytmusic.get_artist_albums(albums_id,params)



    with open('result.json','w',encoding='utf-8') as file:
        json.dump(ytmusic.get_album(albums[0]['browseId']),file,indent=4,ensure_ascii=False)

    # Fetch artist's albums

    return [(album['title'],album['year'],album['browseId']) for album in albums]

# artist_name = input("Enter the artist's name: ")
# albums = get_artist_albums(artist_name)
# for title,year, album_id in albums:
#     print(f"Album: {title}, Year: {year} Album ID: {album_id}")


    

# track_name = input("Enter the track name: ")
# views = get_track_details(track_name)
# print(f"Views for {track_name}: {views}")


song_name = input("Enter the name of the song: ")
lyrics = get_song_lyrics(song_name)
print(lyrics)


@retry_on_error(max_retries=3,till_done=True, delay=2, exceptions=(Exception))
def search_song(song_name):
    print('hello')
    return ytmusic.search(song_name, filter="songs")

# for i in range(100):
#     results = search_song("Imagine")

# if results:
#     for song in results:
#         print(song['title'])

 
from ytmusicapi import YTMusic
import json

ytmusic = YTMusic()  # Without authentication



search_results = ytmusic.search('Marlin Manson', filter='artists')

artist_browseId = search_results[0]['browseId']

# 2. Get the artist's albums
artist_albums = ytmusic.get_artist(artist_browseId)['albums']

# Print the titles of the albums
for album in artist_albums['results'][0:1]:

    album_tracks = ytmusic.get_album(album['browseId'])

    for track in album_tracks['tracks'][0:1]:
        print("Track:", track['title'],track['videoId'])
        track_details = ytmusic.get_song(track['videoId'])
        
        with open('result.json','w',encoding='utf-8') as file:
            json.dump(track_details,file,indent=4,ensure_ascii=False)





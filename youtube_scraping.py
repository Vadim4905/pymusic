#pytube
from pytube import YouTube
yt = YouTube('https://youtu.be/9bZkp7q19f0').streams.filter(only_audio=True).first().download()
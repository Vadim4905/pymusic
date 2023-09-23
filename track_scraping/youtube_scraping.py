#pytube
from pytube import YouTube
# yt = YouTube('https://www.youtube.com/watch?v=VQHTROo0S8E').streams.filter(only_audio=True).first().download()

yt = YouTube('https://www.youtube.com/watch?v=VQHTROo0S8E')
video_stream = yt.streams.get_highest_resolution()

# Download video
video_stream.download()
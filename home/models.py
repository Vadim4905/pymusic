from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
import uuid

# Create your models here.



class Artist(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    name = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='photos')

    def __str__(self):
        return self.name

class Album(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    name = models.CharField(max_length=50)
    artist = models.ForeignKey(Artist,on_delete=models.CASCADE) 
    cover = models.ImageField(upload_to='photos')

    def __str__(self):
        return self.name

class Music(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    name = models.CharField(max_length=50)
    artist = models.ForeignKey(Artist,on_delete=models.CASCADE) 
    album = models.ForeignKey(Album,on_delete=models.CASCADE) 
    created = models.DateField()
    track = models.FileField(upload_to='audios/')
    # publick = publick or private
    # playlist_item = models.ForeignKey(Playlist,on_delete=models.CASCADE) 
    
    def __str__(self):
        return self.name


class Playlist(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    name = models.CharField(max_length=50)
    ispublick = models.BooleanField(default=True)
    musics = models.ManyToManyField(Music)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.name




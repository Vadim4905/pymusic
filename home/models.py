from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
import uuid
from django.db.models.signals import post_delete
from django.dispatch import receiver
import os
from datetime import date

# Create your models here.



class Artist(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    name = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='photos')
    description = models.TextField()

    def __str__(self):
        return self.name

class Album(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    name = models.CharField(max_length=50)
    artist = models.ForeignKey(Artist,on_delete=models.CASCADE) 
    cover = models.ImageField(upload_to='photos')
    year = models.IntegerField()
    duration = models.CharField(max_length=50)
    trackCount = models.IntegerField()
    duration_seconds = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return self.name


def upload_to(instance, filename):
    return os.path.join('audios', instance.artist.name, instance.album.name, filename)  

class Music(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    name = models.CharField(max_length=50)
    artist = models.ForeignKey(Artist,on_delete=models.CASCADE) 
    album = models.ForeignKey(Album,on_delete=models.CASCADE) 
    track = models.FileField(upload_to=upload_to)
    lyrics = models.TextField()
    viewCount = models.IntegerField()
    # publick = publick or private
    class Meta:
        ordering = ['-viewCount']
    
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


@receiver(post_delete, sender=Album)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.cover:
        instance.cover.delete(save=False)

@receiver(post_delete, sender=Artist)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.photo:
        instance.photo.delete(save=False)

@receiver(post_delete, sender=Music)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.track:
        instance.track.delete(save=False)



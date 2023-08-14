from django.forms import ModelForm, Textarea
from django.contrib.admin.widgets import AdminDateWidget, AdminTimeWidget, AdminSplitDateTime
from . import models


class MusicForm(ModelForm):

    class Meta:
        model = models.Music
        fields = (
            "name",
            "artist",
            'album',
            'created',
            'track',
        )
        widgets={
            "created": AdminDateWidget()

        }

class ArtistForm(ModelForm):

    class Meta:
        model = models.Artist
        fields = (
            "name",
            "photo",
        )


class MusicForm(ModelForm):

    class Meta:
        model = models.Music
        fields = (
            "name",
            'track',
            'created',
        )
        widgets={
            "created": AdminDateWidget()
        }

class AlbumForm(ModelForm):

    class Meta:
        model = models.Album
        fields = (
            "name",
            'cover',
            
        )

class PLaylistForm(ModelForm):

    class Meta:
        model = models.Playlist
        fields = (
            "name",
        )

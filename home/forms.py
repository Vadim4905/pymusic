from django.forms import ModelForm, Textarea
from django.contrib.admin.widgets import AdminDateWidget, AdminTimeWidget, AdminSplitDateTime
from . import models


class MusicForm(ModelForm):

    class Meta:
        model = models.Music
        fields = (
            "name",
            'track',
            'lyrics',
            'viewCount',
        )

class ArtistForm(ModelForm):

    class Meta:
        model = models.Artist
        fields = (
            "name",
            "photo",
            'description',
        )


class AlbumForm(ModelForm):

    class Meta:
        model = models.Album
        fields = (
            "name",
            'cover',
            'year',
            'duration',
            'trackCount',
            'duration_seconds',
            'description',
        )
        # widgets={
        #     "year": AdminDateWidget()

        # }

class PLaylistForm(ModelForm):

    class Meta:
        model = models.Playlist
        fields = (
            "name",
        )

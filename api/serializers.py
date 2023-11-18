from rest_framework import serializers

from home import models


class MusicSerializer(serializers.ModelSerializer):
    # category = serializers.ReadOnlyField()

    class Meta:
        model = models.Music
        fields = "__all__"
        # fields = ("category", "name", "image",)

class PlaylistSerializer(serializers.ModelSerializer):
    # category = serializers.ReadOnlyField()

    class Meta:
        model = models.Playlist
        fields = "__all__"
        # fields = ("category", "name", "image",)
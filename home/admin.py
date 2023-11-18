from django.contrib import admin
from home import models

# Register your models here.

class AlbumInline(admin.TabularInline):
    model = models.Album

class ArtistAdmin(admin.ModelAdmin):
    inlines = [AlbumInline, ]
    list_display = ("name", "photo",)

class MusicAdmin(admin.ModelAdmin):
    pass
    # list_filter = ('viewCount',)

class Musicnline(admin.TabularInline):
    model = models.Music

class AlbumAdmin(admin.ModelAdmin):
    inlines = [Musicnline, ]
    list_display = ("name", "cover",'artist')


admin.site.register(models.Music,MusicAdmin)
admin.site.register(models.Playlist)
admin.site.register(models.Album,AlbumAdmin)
admin.site.register(models.Artist,ArtistAdmin)

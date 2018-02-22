from django.urls import path

from album.views import album_list

app_name = 'album'
urlpatterns = [
    path('', album_list, name='album-list'),
]
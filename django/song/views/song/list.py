from django.shortcuts import render

from song.models import Song

__all__ = (
    'song_list',
)


def song_list(request):

    songs = Song.objects.all()
    context = {
        'songs': songs,
    }
    return render(
        request,
        'song/song_list.html',
        context,
    )

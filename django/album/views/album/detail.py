from django.shortcuts import get_object_or_404, render

from album.models import Album

__all__ = (
    'album_detail',
)


def album_detail(request, album_pk):

    album = get_object_or_404(Album, pk=album_pk)
    context = {
        'album': album,
    }
    return render(request, 'album/album_detail.html', context)
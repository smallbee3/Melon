from django.shortcuts import render

from album.models import Album


def album_list(request):

    albums = Album.objects.all()
    context = {
        'albums': albums,
    }
    return render(request, 'album/album_list.html', context)


# def search_album_from_melon(request):
#     pass
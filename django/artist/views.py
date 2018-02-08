from django.shortcuts import render

from artist.models import Artist


def artist_list(request):

    artists = Artist.objects.all()
    context = {
        'artists': artists,

    }
    return render(
        request,
        'artist/artist_list.html',
        context,
    )
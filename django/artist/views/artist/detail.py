from django.shortcuts import get_object_or_404, render

from artist.models import Artist


def artist_detail(request, artist_pk):

    artist = get_object_or_404(Artist, pk=artist_pk)
    context = {
        'artist': artist,
    }
    return render(request, 'artist/artist_detail.html', context)
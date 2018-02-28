from django.shortcuts import get_object_or_404, render

from artist.models import Artist
from crawler.video import video_list_crawler

__all__ = (
    'artist_detail',
)


def artist_detail(request, artist_pk):
    # artist_pk에 해당하는 Artist정보 보여주기
    # Template: artist/artist_detail.html
    # URL: /3/
    artist = get_object_or_404(Artist, pk=artist_pk)
    result = video_list_crawler(artist.name)

    # result

    context = {
        'artist': artist,
        'video_info_list': result,

    }
    return render(request, 'artist/artist_detail.html', context)
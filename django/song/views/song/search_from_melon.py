from django.shortcuts import render

from crawler.song import song_list_crawler
from song.models import Song

__all__ = (
    'song_search_from_melon',
)


def song_search_from_melon(request):

    q = request.GET.get('keyword')

    result = song_list_crawler(q)
    context = {
        "result": result,
    }
    return render(request, 'song/song_search_from_melon.html', context)

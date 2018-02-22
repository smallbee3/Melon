from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET, require_POST

from artist.models import Artist
from crawler.album import album_detail_crawler
from crawler.song import song_detail_crawler

from album.models import Album
from ...models import Song


# @require_POST
def song_add_from_melon(request):
    '''
    패키지 분할 (artist랑 똑같은 형태로)
    artist_add_from_melon과 같은 기능을 함
       song_search_from_melon도 구현
           -> 이 안에 'DB에 추가'하는 Form구현
    '''
    if request.method == 'POST':

        """
        이것과 마지막에

          return redirect('song:song-list')
        else:
          return render(request, '405.html', status=405)

        이것 할 필요가 없이 한줄로 끝냄
        ->
        @require_POST
        """
        # print(request.POST)
        song_id = request.POST.get('song_id')

        result = song_detail_crawler(song_id)


        # 아래의 album 생성하는 코드는 song/models.py에서
        # Song의 Manager를 커스터마이징 하는 부분에 같이 포함시켜서 옮김.

        # album_id = result.get('album_id')
        # album_info = album_detail_crawler(album_id)
        # album, created = Album.objects.get_or_create(
        #     album_id=album_id,
        #     defaults={
        #         "title": album_info.get("album_title"),
        #         "img_cover": album_info.get('album_cover'),
        #         "release_date": datetime.strptime(album_info.get('rel_date'), '%Y.%m.%d')
        #     }
        # )

        artist_id = result.get('melon_id')
        # 2/22 이곳에 크롤링을 포함한 Artist 생성 코드 전부를 복사했다가
        # artist/models.py에서 ArtistManager를 커스터마이징해서 간단하게 코드정리
        #
        # artist = Artist.objects.update_or_create_from_melon(artist_id)
        # -> 이렇게 했다가 artist에 return되는 튜플이 저장되어서 아래에서 에러 발생.
        artist, artist_created = Artist.objects.update_or_create_from_melon(artist_id)


        # song, created = Song.objects.update_or_create(
        #     song_id=song_id,
        #     defaults={
        #         'title': result.get('title'),
        #         'genre': result.get('genre'),
        #         'lyrics': result.get('lyrics'),
        #         'album': album,
        #     }
        # )
        song, song_created = Song.objects.update_or_create_from_melon(song_id)


        # 2/22 Song model에 artists 추가
        song.artists.add(artist)

        return redirect('song:song-list')
    else:
        return render(request, '405.html', status=405)
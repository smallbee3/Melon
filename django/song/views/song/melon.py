from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET, require_POST

from album.models import Album
from crawler.album import album_detail_crawler
from crawler.song import song_list_crawler, song_detail_crawler
from song.models import Song


# @require_GET
# 나중에 get이랑 post랑 나눌일이 있을 때
# 유용하게 사용


# 필요성
# 1)
# -> get만 받을 때 post로 보내면
# -> 500은 어떤 에러가 났는지 알 수 없음.
# -> 500이 뜬다는 거는
# -> value error하면 서버가 멈춰버림.
# 서버가 이 것에 대해서 처리를 해 주고 있다느 ㄴ의미
# 서버가 요청을 처리를 했는데 데이터가 없는것.
# 500대가 오면 서버가 문제가 있는것.

# 500번이면 나서는 안되는 에러가 남.
# 서버가 정상 작동을 하지 못한것
# 404 - 데이터가 없어서 보여줄게 없는 것.
# 403 - forbidden -> 서버가 허용하지 않는 것.
# ex) (melon)에서 require_login 이런게 403에러

# DEBUG = True로 해서 지금은 못보고 있음.
# 404가 나면 404.html을 뿌려줌
# 그걸 오버라이드 할 수 있음.
# 템플릿 폴더 최상에다가 404.html


# 2)
# 페이지 레이아웃을 통일 시킬 수 있음

# 3)
# 만약에 forbidden이면 회원가입 폼을 갖다 놓을 수 있고



__all__ = [
    'song_add_from_melon',
    'song_search_from_melon',
]



def song_search_from_melon(request):
    q = request.GET.get('keyword')

    result = song_list_crawler(q)
    context = {
        "result": result
    }
    return render(request, 'song/song_search_from_melon.html', context)


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
        print(request.POST)
        song_id = request.POST.get('song_id')

        result = song_detail_crawler(song_id)

        album_id = result.get('album_id')
        album_info = album_detail_crawler(album_id)

        album, created = Album.objects.get_or_create(
            album_id=album_id,
            defaults={
                "title": album_info.get("album_title"),
                "img_cover": album_info.get('album_cover'),
                "release_date": datetime.strptime(album_info.get('rel_date'), '%Y.%m.%d')
            }
        )

        # # 1단계
        # Song.objects.create(
        #     song_id=song_id,
        #     title=title,
        #     genre=genre,
        #     lyrics=lyrics,
        # )
        song, created = Song.objects.update_or_create(
            song_id=song_id,
            defaults={
                'title': result.get('title'),
                'genre': result.get('genre'),
                'lyrics': result.get('lyrics'),
                'album': album,
            }
        )
        return redirect('song:song-list')
    else:
        return render(request, '405.html', status=405)

    #
    # ->  status를 써주어야 함, 왜냐하면 405.html이 아니라 다른 song_list.html
    # 이렇게 가면 에러임에도 그냥 정상적으로 해당 페이지로 이동하는 것이 되기 때문.
    # -> 이 때문에 그냥 정상 페이지를 render할 때 status를 404로 써주면
    # 아무 이상없는데 chrome에서 network의 header를 보면 404 warning이
    # 뜨는 것을 확인할 수 있다.


    #################################################
    # 만약 album/views.py에서 똑같이 DB 저장 로직을 짠다면
    #
    # album, created = Album.objects.update_or_create(
    #
    # song, created = Song.objects.get_or_create(
    #
    # 의 순서대로 작성함.
    # Album을 먼저 update_or_create하고 Song을 그 다음
    # get_or_create하는 이유는 만들어진 Album에 Song을 넣어주기
    # 위함임.
    # Song을 Album에 넣어줄 때 Song이 한 곡일 수도 여러곡 일 수도 있으니
    # for문 안에 get_or_create를 통해 Album에 넣어준다.
    # 이때 기존에 이미 생성한 Song을 get으로 가져온 경우에는
    # create의 마지막에서 'album': album으로 album 객체를
    # 만들어주는 것과 같은 작업을 추가해 주어야 한다.
    #################################################

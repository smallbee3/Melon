from django.shortcuts import redirect

from album.models import Album

__all__ = (
    'album_add_from_melon',
)


def album_add_from_melon(request):
    """
    1. artist_search_from_melon.html에
        form을 작성 (action이 현재 이 view로 올 수 있도록), POST메서드
            필요한 요소는 csrf_token과
                type=hidden으로 전달하는 artist_id값
                <input type="hidden" value="{{ artist_info.artist_id }}">
                button submit (추가하기)
    2. 작성한 form
    POST요청을 받음 (추가하기 버튼 클릭)
    request.POST['artist_id']
    :param request:
    :return:
    """
    if request.method == 'POST':
        album_id = request.POST.get('album_id')
        Album.objects.update_or_create_from_melon(album_id)
    return redirect('album:album-list')
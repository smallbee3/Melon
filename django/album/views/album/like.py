from django.shortcuts import redirect

from album.models import Album

__all__ = (
    'album_like_toggle',
)


def album_like_toggle(request, album_pk):

    album = Album.objects.get(pk=album_pk)

    if request.method == 'POST':

        # album.toggle_like_user(user=request.user)
        # 의미가 이상해서 아래로 함.
        request.user.toggle_like_album(album=album)

        # return redirect('album:album-list')

        # artist_detail에서 like_toggle시 원래 페이지로 갈 수 있도록 next-path값 추가
        next_path = request.POST.get('next-path', 'album:album-list')
        return redirect(next_path)

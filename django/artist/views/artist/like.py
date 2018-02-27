from django.shortcuts import redirect

from artist.models import Artist

__all__ = (
    'artist_like_toggle',
)


def artist_like_toggle(request, artist_pk):
    """
    request.user와
    artist_pk를 사용해서

    ArtistLike객체를 토글하는 뷰
        -> POST요청에서 동작

    완료 후에는 artist:artist-list로 이동
    """
    artist = Artist.objects.get(pk=artist_pk)

    if request.method == 'POST':
        artist.toggle_like_user(user=request.user)
        # return redirect('artist:artist-list')

        # artist_detail에서 like_toggle시 원래 페이지로 갈 수 있도록 next-path값 추가
        next_path = request.POST.get('next-path', 'artist:artist-list')
        return redirect(next_path)

from django.shortcuts import redirect

from artist.models import Artist


def artist_like_toggle(request, artist_pk):
    """
    request.user와
    artist_pk를 사용해서

    ArtistLike객체를 토글하는 뷰

    완료 후에는 artist:artist-list로 이동

    :param request:
    :param artist_pk:
    :return:
    """

    artist = Artist.objects.get(pk=artist_pk)

    if request.method == 'POST':
        artist.toggle_like_user(user=request.user)
        next_path = request.POST.get('next-path', 'artist:artist-list')
        return redirect(next_path)


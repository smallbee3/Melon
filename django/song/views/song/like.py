from django.shortcuts import redirect, get_object_or_404

from song.models import Song

__all__ = (
    'song_like_toggle',
)


def song_like_toggle(request, song_pk):

    song = get_object_or_404(Song, pk=song_pk)

    if request.method == 'POST':

        # song.toggle_like_user(user=request.user)
        # 의미가 이상해서 아래로 함.
        request.user.toggle_like_song(song=song)

        # 2/26 과제할 때 이해하며 짠 코드
        # if not request.POST.get('next-path'):
        #     return redirect('song:song-list')
        # return redirect(request.POST.get('next_path'))

        next_path = request.POST.get('next-path', 'song:song-list')
        return redirect(next_path)

from django.shortcuts import get_object_or_404, render, redirect

from song.forms import SongForm
from song.models import Song

__all__ = (
    'song_edit',
)


def song_edit(request, song_pk):
    song = get_object_or_404(Song, pk=song_pk)

    if request.method == 'POST':
        form = SongForm(request.POST, instance=song)
        if form.is_valid():
            form.save()
            return redirect('song:song-list')

    else:
        form = SongForm(instance=song)

    context = {
        'song_form': form,
        'song': song,
    }
    return render(request, 'song/song_edit.html', context)

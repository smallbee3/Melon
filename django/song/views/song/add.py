from django.shortcuts import render, redirect

from song.forms import SongForm


__all__ = (
    'song_add',
)


def song_add(request):
    if request.method == 'POST':
        forms = SongForm(request.POST, request.FILES)
        if forms.is_valid():
            forms.save()
            return redirect('song:song-list')

    else:
        forms = SongForm()
    context = {
        'song_form': forms,
    }
    return render(request, 'song/song_add.html', context)

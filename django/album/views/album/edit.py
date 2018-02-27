from django.shortcuts import get_object_or_404, render, redirect

from album.forms import AlbumForm
from album.models import Album

__all__ = (
    'album_edit',
)


def album_edit(request, album_pk):
    album = get_object_or_404(Album, pk=album_pk)

    if request.method == 'POST':
        form = AlbumForm(request.POST, instance=album)
        if form.is_valid():
            form.save()
            return redirect('album:album-list')

    else:
        form = AlbumForm(instance=album)

    context = {
        'album_form': form,
        'album': album,
    }
    return render(request, 'album/album_edit.html', context)

from django.shortcuts import redirect, render

from album.forms import AlbumForm

__all__ = (
    'album_add',
)


def album_add(request):
    if request.method == 'POST':
        form = AlbumForm(request.POST, request.FILES)
        print('검문소1')
        if form.is_valid():
            form.save()
            print('검문소2')
            return redirect('album:album-list')
    else:
        form = AlbumForm()

    context = {
        'album_form': form,
    }
    return render(request, 'album/album_add.html', context)


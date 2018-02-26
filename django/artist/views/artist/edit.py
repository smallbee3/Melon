from django.shortcuts import redirect, render, get_object_or_404

from artist.forms import AritstForm
from artist.models import Artist


def artist_edit(request, artist_pk):
    """
    artist_pk에 해당하는 Artist를 수정

    Form: ArtistForm
    Template: artist/artist-edit.html

    bound form: Artist(instace=<artist instance>)
    ModelForm을 사용해 instance 업데이트
        form = ArtistForm(request.POST, request.FILES, instace=<artist instance>)
        form.save()

    :param request:
    :param artist_pk:
    :return:
    """
    # artist = Artist.objects.get(pk=artist_pk)
    artist = get_object_or_404(Artist, pk=artist_pk)

    if request.method == 'POST':
        form = AritstForm(request.POST, request.FILES, instance=artist)
        if form.is_valid():
            form.save()
            return redirect('artist:artist-list')
    else:
        # form = AritstForm(request.POST, request.FILES, instance=artist)
        form = AritstForm(instance=artist)
        # bound form

    context = {
        'artist_form': form,
        'artist_pk': artist_pk,
    }
    return render(request, 'artist/artist_edit.html', context)


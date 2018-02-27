from django import forms

from album.models import Album

__all__ = (
    'AlbumForm',
)


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = [
            'album_id',
            'title',
            'img_cover',
            'release_date',
        ]

        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            )
        }
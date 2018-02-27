from django import forms

from song.models import Song


__all__ = (
    'SongForm',
)


class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = [
            'song_id',
            'title',
            'genre',
            'lyrics',
        ]

        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            )
        }
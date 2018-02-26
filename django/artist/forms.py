# from django.forms import ModelForm
from django import forms

from artist.models import Artist


class AritstForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = [
            # 'melon_id',
            'img_profile',
            'name',
            'real_name',
            'nationality',
            'birth_date',
            'constellation',
            'blood_type',
            'intro',
        ]

        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            )
        }

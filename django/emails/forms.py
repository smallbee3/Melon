from django import forms

from emails.models import Emails


class EmailsForm(forms.ModelForm):
    class Meta:
        model = Emails
        fields = [
            'email_to',
            'subject_text',
            'body_text',
        ]

        widgets = {
            'email_to': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            )
        }
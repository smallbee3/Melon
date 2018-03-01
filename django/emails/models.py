from django.db import models


class Emails(models.Model):
    email_to = models.CharField(
        'To',
        max_length=100,
    )
    subject_text = models.CharField(
        'subject',
        max_length=300,
    )
    body_text = models.TextField(
        'body',
        max_length=3000,
    )
    created_date = models.DateTimeField(auto_now_add=True)

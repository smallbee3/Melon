# Generated by Django 2.0.2 on 2018-02-27 01:25

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('song', '0002_auto_20180227_0616'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='like_users',
            field=models.ManyToManyField(blank=True, related_name='like_songs', through='song.SongLike', to=settings.AUTH_USER_MODEL),
        ),
    ]

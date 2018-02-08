# Generated by Django 2.0.2 on 2018-02-07 22:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('song', '0003_auto_20180208_0703'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='album',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='album.Album', verbose_name='가수'),
        ),
        migrations.AlterField(
            model_name='song',
            name='artist',
            field=models.ManyToManyField(through='song.ArtistSong', to='artist.Artist', verbose_name='가수'),
        ),
    ]

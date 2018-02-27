# Generated by Django 2.0.2 on 2018-02-26 23:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('album', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AlbumLike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_data', models.DateTimeField(auto_now_add=True)),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='like_user_info_list', to='album.Album')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='like_album_info_list', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='album',
            name='like_users',
            field=models.ManyToManyField(blank=True, related_name='like_albums', through='album.AlbumLike', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='albumlike',
            unique_together={('album', 'user')},
        ),
    ]

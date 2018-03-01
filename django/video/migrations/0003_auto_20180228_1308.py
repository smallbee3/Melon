# Generated by Django 2.0.2 on 2018-02-28 04:08

from django.db import migrations, models
import video.models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0002_auto_20180228_1130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='thumbnail',
            field=models.ImageField(blank=True, upload_to=video.models.dynamic_video_thumbnail_path, verbose_name='Thumbnail image'),
        ),
    ]

# Generated by Django 2.0.2 on 2018-02-07 23:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artist', '0004_auto_20180208_0705'),
    ]

    operations = [
        migrations.AddField(
            model_name='artist',
            name='member',
            field=models.CharField(blank=True, max_length=100, verbose_name='멤버'),
        ),
    ]

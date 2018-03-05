# Generated by Django 2.0.2 on 2018-03-04 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Emails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_to', models.CharField(max_length=100, verbose_name='To')),
                ('subject_text', models.CharField(max_length=300, verbose_name='subject')),
                ('body_text', models.TextField(max_length=3000, verbose_name='body')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]

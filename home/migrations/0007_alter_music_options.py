# Generated by Django 4.2.1 on 2023-11-18 17:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_alter_music_track'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='music',
            options={'ordering': ['-viewCount']},
        ),
    ]

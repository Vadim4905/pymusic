# Generated by Django 4.2.1 on 2023-11-13 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_remove_music_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='year',
            field=models.IntegerField(),
        ),
    ]

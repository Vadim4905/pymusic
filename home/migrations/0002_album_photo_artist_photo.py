# Generated by Django 4.2.1 on 2023-08-09 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='photo',
            field=models.ImageField(default='None', upload_to='photos'),
        ),
        migrations.AddField(
            model_name='artist',
            name='photo',
            field=models.ImageField(default='None', upload_to='photos'),
        ),
    ]
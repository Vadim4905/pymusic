# Generated by Django 4.2.1 on 2023-11-13 02:47

from django.db import migrations, models
import home.models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_alter_album_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='music',
            name='track',
            field=models.FileField(upload_to=home.models.upload_to),
        ),
    ]
# Generated by Django 4.2.7 on 2023-11-22 02:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0008_catalogue_images'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='catalogue',
            name='images',
        ),
        migrations.AddField(
            model_name='catalogue',
            name='mages',
            field=models.ImageField(null=True, upload_to='img_catalogue/'),
        ),
    ]

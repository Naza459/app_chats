# Generated by Django 4.0.4 on 2023-10-04 23:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='conversations',
            name='is_closed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='historyconversations',
            name='is_closed',
            field=models.BooleanField(default=False),
        ),
    ]

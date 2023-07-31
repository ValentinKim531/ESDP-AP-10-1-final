# Generated by Django 4.2.2 on 2023-07-27 05:57

import chat.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_chatmessage_file_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='is_audio',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='chatroom',
            name='chat_type',
            field=models.CharField(choices=[('PRIVATE', 'Private'), ('GROUP', 'Group'), ('CHANNEL', 'Channel')], default=chat.models.ChatType['PRIVATE'], max_length=7),
        ),
    ]
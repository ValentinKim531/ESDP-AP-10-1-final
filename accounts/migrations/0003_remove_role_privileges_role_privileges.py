# Generated by Django 4.2.2 on 2023-07-24 15:16

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='role',
            name='privileges',
        ),
        migrations.AddField(
            model_name='role',
            name='privileges',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, choices=[('ALLOW_TO_ALL_RESIDENTS', 0), ('ALLOW_EVENT_CREATE', 1), ('ALLOW_EVENT_UPDATE', 2), ('ALLOW_EVENT_DELETE', 3), ('ALLOW_NEWS_CREATE', 4), ('ALLOW_NEWS_UPDATE', 5), ('ALLOW_NEWS_DELETE', 6), ('ALLOW_REQUEST_CREATE', 7), ('ALLOW_REQUEST_UPDATE', 8), ('ALLOW_REQUEST_DELETE', 9), ('ALLOW_REQUEST_FROM_ALL_RESIDENT_READ', 10), ('ALLOW_REQUEST_WRITE_RESPONSE', 11), ('ALLOW_RESIDENT_BOOKED_READ', 12), ('ALLOW_RESIDENT_BOOKING', 13), ('ALLOW_VOTE_CREATE', 14)], max_length=2000, null=True, verbose_name='привилегия'), blank=True, null=True, size=None),
        ),
    ]

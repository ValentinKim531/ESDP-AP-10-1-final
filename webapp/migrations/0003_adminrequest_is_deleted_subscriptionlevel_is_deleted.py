# Generated by Django 4.2.2 on 2023-07-04 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0002_rename_closing_at_adminrequest_closed_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='adminrequest',
            name='is_deleted',
            field=models.BooleanField(default=False, verbose_name='Удалено'),
        ),
        migrations.AddField(
            model_name='subscriptionlevel',
            name='is_deleted',
            field=models.BooleanField(default=False, verbose_name='Удалено'),
        ),
    ]

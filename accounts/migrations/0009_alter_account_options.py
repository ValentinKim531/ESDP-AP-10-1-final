# Generated by Django 4.2.2 on 2023-06-20 06:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_remove_account_dislikes_qty_account_achievements_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='account',
            options={'ordering': ['first_name'], 'verbose_name': 'Профиль', 'verbose_name_plural': 'Профили'},
        ),
    ]

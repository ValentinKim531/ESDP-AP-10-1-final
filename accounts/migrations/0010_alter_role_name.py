# Generated by Django 4.2.2 on 2023-07-26 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_alter_role_privileges'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='name',
            field=models.CharField(max_length=30, unique=True, verbose_name='Роль'),
        ),
    ]

# Generated by Django 4.1.4 on 2022-12-25 19:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_alter_task_options_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='bio',
        ),
    ]

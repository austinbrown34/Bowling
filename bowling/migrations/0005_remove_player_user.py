# Generated by Django 2.0.7 on 2018-07-13 16:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bowling', '0004_player_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='user',
        ),
    ]

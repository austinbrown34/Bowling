# Generated by Django 2.0.7 on 2018-07-09 12:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bowling', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GamePlayer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='bowling.Game')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='bowling.Player')),
            ],
            options={
                'verbose_name': 'GamePlayer',
                'verbose_name_plural': 'GamePlayers',
            },
        ),
        migrations.RemoveField(
            model_name='playergame',
            name='game',
        ),
        migrations.AlterField(
            model_name='playergame',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='bowling.GamePlayer'),
        ),
        migrations.AddField(
            model_name='game',
            name='players',
            field=models.ManyToManyField(through='bowling.GamePlayer', to='bowling.Player'),
        ),
    ]

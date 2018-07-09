from django.db import models


class Player(models.Model):
    name = models.CharField(max_length=5)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Player'
        verbose_name_plural = 'Players'

    def __str__(self):
        return '{}'.format(
            self.name
        )


class Frame(models.Model):
    number = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Frame'
        verbose_name_plural = 'Frames'

    def __str__(self):
        return '{}'.format(
            self.number
        )


class Chance(models.Model):
    number = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Chance'
        verbose_name_plural = 'Chances'

    def __str__(self):
        return '{}'.format(
            self.number
        )


class Game(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Game'
        verbose_name_plural = 'Games'

    def __str__(self):
        return '{}'.format(
            self.date_created
        )


class PlayerGame(models.Model):
    player = models.ForeignKey(Player, on_delete=models.PROTECT)
    game = models.ForeignKey(Game, on_delete=models.PROTECT)
    mark = models.CharField(max_length=2)
    frame = models.ForeignKey(Frame, on_delete=models.PROTECT)
    chance = models.ForeignKey(Chance, on_delete=models.PROTECT)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'PlayerGame'
        verbose_name_plural = 'PlayerGame'

    def __str__(self):
        return '{}({}) - ({}/{}) - {}'.format(
            self.player,
            self.game,
            self.frame,
            self.chance,
            self.mark
        )

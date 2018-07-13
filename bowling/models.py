from django.db import models
from django.core.exceptions import ObjectDoesNotExist


TOTAL_FRAMES = 10
FRAME_CHANCES = {
    1: 2,
    2: 2,
    3: 2,
    4: 2,
    5: 2,
    6: 2,
    7: 2,
    8: 2,
    9: 2,
    10: 3
}


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
    players = models.ManyToManyField(Player, through="GamePlayer")
    current_frame = models.IntegerField(default=0)
    current_chance = models.IntegerField(default=0)
    current_player_index = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Game'
        verbose_name_plural = 'Games'

    def __str__(self):
        return '{}'.format(
            self.date_created
        )

    @staticmethod
    def total_frames():
        return TOTAL_FRAMES

    @staticmethod
    def frame_chances(frame_number):
        return FRAME_CHANCES[frame_number]

    @staticmethod
    def max_chances():
        return max(FRAME_CHANCES.items())[1]

    @staticmethod
    def chance_points(chance):
        if chance == 'x' or chance == '/':
            return 10
        else:
            return int(chance)

    @staticmethod
    def calculate_score(marks):
        score = 0
        x = 0
        while x < len(marks) - 1:
            if marks[x] == 'x':
                try:
                    if marks[x + 2] == '/':
                        score += 20
                    else:
                        score += (
                            10 +
                            Game.chance_points(marks[x + 1]) +
                            Game.chance_points(marks[x + 2])
                        )
                except Exception:
                    pass
                x += 1
            elif marks[x + 1] == '/':
                try:
                    score += (
                        10 + Game.chance_points(marks[x + 2])
                    )
                except Exception:
                    pass
                x += 2
            else:
                score += (
                    Game.chance_points(marks[x]) +
                    Game.chance_points(marks[x + 1])
                )
                x += 2
        return score

    @property
    def number_of_players(self):
        return len(self.players.all())

    @property
    def current_player(self):
        if self.number_of_players:
            return self.players.all()[self.current_player_index]
        else:
            return None

    @property
    def is_game_over(self):
        if self.number_of_players:
            last_player = self.players.last()
            game_player = self.get_gameplayer(last_player)
            try:
                PlayerGame.objects.get(
                    player=game_player,
                    frame__number=Game.total_frames(),
                    chance__number=Game.frame_chances(Game.total_frames())
                )
                return True
            except ObjectDoesNotExist:
                pass
        return False

    @property
    def has_game_begun(self):
        if self.current_frame:
            return True
        return False

    @property
    def is_game_active(self):
        if self.has_game_begun and not self.is_game_over:
            return True
        return False

    def get_state(self):
        return {
            'frame': self.current_frame,
            'chance': self.current_chance,
            'player': self.current_player,
            'scores': self.get_scores()
        }

    def get_gameplayer(self, player):
        try:
            game_player = GamePlayer.objects.get(
                player=player,
                game=self
            )
            return game_player
        except ObjectDoesNotExist:
            return None

    def start(self):
        self.current_frame = 1
        self.current_chance = 1

    def reset_current_chance(self):
        self.current_chance = 1

    def next_player(self):
        if self.current_player_index == self.number_of_players - 1:
            self.current_player_index = 0
        else:
            self.current_player_index += 1

    def next_frame(self):
        if self.current_frame < Game.total_frames():
            self.current_frame += 1
            self.reset_current_chance()

    def extra_chance(self, prev_mark):
        if self.current_chance < Game.frame_chances(self.current_frame):
            if self.current_frame == Game.total_frames():
                if self.current_chance == 1:
                    return True
                elif self.current_chance != 1 and prev_mark in ['/', 'x']:
                    return True
                else:
                    return False
            else:
                if prev_mark in ['/', 'x']:
                    return False
                else:
                    return True
        return False

    def next(self, prev_mark):
        if self.is_game_active:
            if self.extra_chance(prev_mark):
                self.current_chance += 1
            else:
                self.next_frame()
                self.next_player()

    def bowl(self, mark):
        if self.is_game_over:
            return 'Game is Over!'
        if not self.has_game_begun:
            return 'Game has not Started!'
        frame = Frame.objects.get(number=self.current_frame)
        chance = Chance.objects.get(number=self.current_chance)
        player_game = PlayerGame.objects.create(
            player=self.get_gameplayer(self.current_player),
            mark=mark,
            frame=frame,
            chance=chance
        )
        self.next(mark)
        return player_game

    def get_player_score(self, game_player):
        return Game.calculate_score(game_player.get_marks_list())

    def get_current_player_score(self):
        game_player = self.get_gameplayer(self.current_player)
        return self.get_player_score(game_player)

    def get_scores(self):
        player_scores = {}
        for i, player in enumerate(self.players.all()):
            player_scores[i] = {
                player.name: self.get_player_score(self.get_gameplayer(player))
            }
        return player_scores


class GamePlayer(models.Model):
    player = models.ForeignKey(Player, on_delete=models.PROTECT)
    game = models.ForeignKey(Game, on_delete=models.PROTECT)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'GamePlayer'
        verbose_name_plural = 'GamePlayers'

    def __str__(self):
        return '{}({})'.format(
            self.player,
            self.game
        )

    def get_game_marks(self):
        game_marks = PlayerGame.objects.filter(
            player=self
        ).order_by('frame', 'chance')
        return game_marks

    def get_marks_list(self):
        marks = []
        game_marks = self.get_game_marks()
        for game_mark in game_marks:
            marks.append(game_mark.mark)
        return marks


class PlayerGame(models.Model):
    player = models.ForeignKey(GamePlayer, on_delete=models.PROTECT)
    mark = models.CharField(max_length=2)
    frame = models.ForeignKey(Frame, on_delete=models.PROTECT)
    chance = models.ForeignKey(Chance, on_delete=models.PROTECT)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'PlayerGame'
        verbose_name_plural = 'PlayerGame'

    def __str__(self):
        return '{} - ({}/{}) - {}'.format(
            self.player,
            self.frame,
            self.chance,
            self.mark
        )

from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save
from django.dispatch import receiver
from tastypie.models import create_api_key

# Constants

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

# Create API Key when User is created
post_save.connect(create_api_key, sender=User)


class Player(models.Model):
    """Player is a User with a name (<= 5 chars) used in Games.

    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
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


@receiver(post_save, sender=User)
def create_user_player(sender, instance, created, **kwargs):
    """Associates User with Player as a One-To-One Relationship.

    """
    if created:
        Player.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_player(sender, instance, **kwargs):
    """Saves player attribute to User.

    """
    instance.player.save()


class Frame(models.Model):
    """Frame represents a bowling frame and is identified by it's number.

    """
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
    """Chance represents one of many chances to bowl within a frame.

    """
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
    """Game has many Players and the state of a bowling game.

    """
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    players = models.ManyToManyField(Player, through="GamePlayer")
    current_frame = models.IntegerField(default=0)
    current_chance = models.IntegerField(default=0)
    current_player_index = models.IntegerField(default=0)
    status = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Game'
        verbose_name_plural = 'Games'

    def __str__(self):
        return '{}'.format(
            self.date_created
        )

    @staticmethod
    def total_frames():
        """Returns int value representing max number of frames in a game.

        """
        return TOTAL_FRAMES

    @staticmethod
    def frame_chances(frame_number):
        """Takes a frame_number and returns max number of chances for that frame.

        """
        return FRAME_CHANCES[frame_number]

    @staticmethod
    def max_chances():
        """Returns the max number of chances for any/all frames.

        """
        return max(FRAME_CHANCES.items())[1]

    @staticmethod
    def chance_points(chance):
        """Takes a str representing a mark on a given chance and returns int value.

        """
        if chance == 'x' or chance == '/':
            return 10
        else:
            return int(chance)

    @staticmethod
    def calculate_score(marks):
        """Takes list of str marks for a Player and returns (int) current score

        """
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
        """Returns int representing number of players for game.

        """
        return len(self.players.all())

    @property
    def current_player(self):
        """Returns current Player or None.

        """
        if self.number_of_players:
            return self.players.all()[self.current_player_index]
        else:
            return None

    @property
    def is_game_over(self):
        """Returns bool representing whether game is over.

        """
        if self.status == -1:
            return True
        return False

    @property
    def has_game_begun(self):
        """Returns bool representing whether game has begun.

        """
        if self.status == 0:
            return False
        return True

    @property
    def is_game_active(self):
        """Returns bool representing whether game is active.

        """
        if self.has_game_begun and not self.is_game_over:
            return True
        return False

    def get_player(self, index):
        """Takes int index and returns Player of game at that index.

        """
        if index < self.number_of_players:
            return self.players.all()[index]
        else:
            return None

    def get_state(self):
        """Returns dict representing current state of game.

        """
        return {
            'frame': self.current_frame,
            'chance': self.current_chance,
            'player': self.current_player,
            'scores': self.get_scores()
        }

    def get_gameplayer(self, player):
        """Takes Player and returns GamePlayer.

        """
        try:
            game_player = GamePlayer.objects.get(
                player=player,
                game=self
            )
            return game_player
        except ObjectDoesNotExist:
            return None

    def start(self):
        """Sets state to start game and returns representation of that state.

        """
        self.current_frame = 1
        self.current_chance = 1
        self.status = 1
        self.save()
        return self.get_state()

    def reset_current_chance(self):
        """Sets current_chance back to 1.

        """
        self.current_chance = 1
        self.save()

    def next_player(self):
        """Updates current_player_index to represent next player.

        """
        if self.current_player_index == self.number_of_players - 1:
            self.current_player_index = 0
        else:
            self.current_player_index += 1
        self.save()

    def next_frame(self):
        """Advances current_frame if less than total_frames.

        """
        if self.current_frame < Game.total_frames():
            self.current_frame += 1
            self.reset_current_chance()
        else:
            self.status = -1
        self.save()

    def extra_chance(self, prev_mark):
        """Takes str prev_mark of Player and returns bool representing whether another chance is given.

        """
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
        """Advances current state to next state.

        """
        if self.is_game_active:
            if self.extra_chance(prev_mark):
                self.current_chance += 1
            else:
                if self.current_player_index == self.number_of_players - 1:
                    self.next_frame()
                else:
                    self.reset_current_chance()
                self.next_player()
        self.save()

    def bowl(self, mark):
        """Takes a str mark and creates and returns PlayerGame.

        """
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
        """Takes GamePlayer and returns int representing current score of Player.

        """
        return Game.calculate_score(game_player.get_marks_list())

    def get_current_player_score(self):
        """Returns current Player's current int score.

        """
        game_player = self.get_gameplayer(self.current_player)
        return self.get_player_score(game_player)

    def get_scores(self):
        """Returns dict representing Players' current scores of game.

        """
        player_scores = {}
        for i, player in enumerate(self.players.all()):
            player_scores[i] = {
                player.name: self.get_player_score(self.get_gameplayer(player))
            }
        return player_scores


class GamePlayer(models.Model):
    """GamePlayer is a representation of the relationship between Player and Game.

    """
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
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
        """Returns PlayerGames for GamePlayer ordered by frame, chance.

        """
        game_marks = PlayerGame.objects.filter(
            player=self
        ).order_by('frame', 'chance')
        return game_marks

    def get_marks_list(self):
        """Returns PlayerGames for GamePlayer ordered by frame, chance as list of marks.

        """
        marks = []
        game_marks = self.get_game_marks()
        for game_mark in game_marks:
            marks.append(game_mark.mark)
        return marks


class PlayerGame(models.Model):
    """PlayerGame represents the stats of a GamePlayer for a specific Frame/Chance.

    """
    player = models.ForeignKey(GamePlayer, on_delete=models.CASCADE)
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

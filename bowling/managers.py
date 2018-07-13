from bowling.models import Frame, Chance, Game, Player, GamePlayer
import re


class GameManager(object):
    @staticmethod
    def new_game(player_names):
        GameManager.setup()
        sanitized_player_names = GameManager.sanitize_player_names(
            player_names
        )
        game = GameManager.create_game()
        GameManager.create_game_players(game, sanitized_player_names)
        return game

    @staticmethod
    def sanitize_player_names(player_names):
        sanitized_player_names = []
        pattern = re.compile('[\W_]+')
        for name in player_names:
            sanitized_player_names.append(
                pattern.sub('', name)[:5]
            )
        return sanitized_player_names

    @staticmethod
    def create_game():
        game = Game.objects.create()
        return game

    @staticmethod
    def create_game_players(game, player_names):
        for name in player_names:
            player, created_player = Player.objects.get_or_create(
                name=name
            )
            gp, created_gp = GamePlayer.objects.get_or_create(
                player=player,
                game=game
            )

    @staticmethod
    def setup():
        GameManager.setup_frames()
        GameManager.setup_chances()

    @staticmethod
    def setup_frames():
        total_frames = Game.total_frames()
        for x in range(1, total_frames + 1):
            obj, created = Frame.objects.get_or_create(
                number=x
            )

    @staticmethod
    def setup_chances():
        max_chances = Game.max_chances()
        for x in range(1, max_chances + 1):
            obj, created = Chance.objects.get_or_create(
                number=x
            )

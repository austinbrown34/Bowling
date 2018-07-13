from bowling.models import Frame, Chance, Game, Player, GamePlayer
import re


class GameManager(object):
    @staticmethod
    def new_game(player_ids):
        GameManager.setup()
        game = GameManager.create_game()
        GameManager.create_game_players(game, player_ids)
        return game

    @staticmethod
    def create_game():
        game = Game.objects.create()
        return game

    @staticmethod
    def create_game_players(game, player_ids):
        for id in player_ids:
            player = Player.objects.get(id=id)
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

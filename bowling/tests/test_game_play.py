from django.test import TestCase
from bowling.models import Player, Game, Frame, Chance
from bowling.managers import GameManager
from django.contrib.auth.models import User


class GamePlayTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='testusera',
            password='12345'
        )
        self.user2 = User.objects.create_user(
            username='testuserb',
            password='12345'
        )
        self.user1.player.name = 'testa'
        self.user2.player.name = 'testb'
        self.player_ids = [
            self.user1.player.id,
            self.user2.player.id
        ]
        self.game = GameManager.new_game(self.player_ids)

    def test_number_of_players_initial(self):
        self.assertEqual(self.game.number_of_players, 2)

    def test_current_player_initial(self):
        self.assertEqual(self.game.current_player, self.user1.player)

    def test_is_game_over_initial(self):
        self.assertEqual(self.game.is_game_over, False)

    def test_has_game_begun_initial(self):
        self.assertEqual(self.game.has_game_begun, False)

    def test_is_game_active_initial(self):
        self.assertEqual(self.game.is_game_active, False)

    def test_get_state_initial(self):
        response = {
            'frame': 0,
            'chance': 0,
            'player': self.game.current_player,
            'scores': {
                0: {self.game.current_player.name: 0},
                1: {self.game.get_player(1).name: 0}
            }
        }
        self.assertEqual(self.game.get_state(), response)

    def test_start(self):
        self.game.start()
        self.assertEqual(self.game.is_game_active, True)
        response = {
            'frame': 1,
            'chance': 1,
            'player': self.game.current_player,
            'scores': {
                0: {self.game.current_player.name: 0},
                1: {self.game.get_player(1).name: 0}
            }
        }
        self.assertEqual(self.game.get_state(), response)

    def test_first_bowl(self):
        self.game.start()
        self.game.bowl('x')
        response = {
            'frame': 1,
            'chance': 1,
            'player': self.game.current_player,
            'scores': {
                0: {self.game.current_player.name: 0},
                1: {self.game.get_player(1).name: 0}
            }
        }
        self.assertEqual(self.game.get_state(), response)

    def test_second_bowl(self):
        self.game.start()
        self.game.bowl('x')
        self.game.bowl('x')
        response = {
            'frame': 2,
            'chance': 1,
            'player': self.game.current_player,
            'scores': {
                0: {self.game.current_player.name: 0},
                1: {self.game.get_player(1).name: 0}
            }
        }
        self.assertEqual(self.game.get_state(), response)

    def test_third_frame_bowl(self):
        self.game.start()
        self.game.bowl('x')
        self.game.bowl('x')
        self.game.bowl('0')
        self.game.bowl('0')
        self.game.bowl('0')
        self.game.bowl('1')
        response = {
            'frame': 3,
            'chance': 1,
            'player': self.game.current_player,
            'scores': {
                0: {self.game.current_player.name: 10},
                1: {self.game.get_player(1).name: 12}
            }
        }
        self.assertEqual(self.game.get_state(), response)

    def test_last_frame_bowl(self):
        self.game.start()
        self.game.bowl('x')
        self.game.bowl('x')
        self.game.bowl('0')
        self.game.bowl('0')
        self.game.bowl('0')
        self.game.bowl('1')
        self.game.bowl('x')
        self.game.bowl('x')
        self.game.bowl('x')
        self.game.bowl('x')
        self.game.bowl('x')
        self.game.bowl('x')
        self.game.bowl('x')
        self.game.bowl('x')
        self.game.bowl('x')
        self.game.bowl('x')
        self.game.bowl('x')
        self.game.bowl('x')
        self.game.bowl('x')
        self.game.bowl('x')
        self.game.bowl('x')
        self.game.bowl('x')
        self.game.bowl('x')
        self.game.bowl('1')
        self.game.bowl('2')
        response = {
            'frame': 10,
            'chance': 2,
            'player': self.game.current_player,
            'scores': {
                0: {self.game.current_player.name: 250},
                1: {self.game.get_player(1).name: 199}
            }
        }
        self.assertEqual(self.game.get_state(), response)
        self.assertEqual(self.game.is_game_over, True)

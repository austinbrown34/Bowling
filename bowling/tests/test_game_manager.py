from django.test import TestCase
from bowling.models import Player, Game, Frame, Chance
from bowling.managers import GameManager
from django.contrib.auth.models import User


class GameManagerTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='testuser',
            password='12345'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            password='12345'
        )
        self.user1.player.name = 'test1'
        self.user2.player.name = 'test2'
        self.player_ids = [
            self.user1.player.id,
            self.user2.player.id
        ]
        self.game = GameManager.new_game(self.player_ids)

    def test_new_game(self):
        game_obj = Game.objects.get(id=self.game.id)
        self.assertEqual(game_obj.id, self.game.id)

    def test_frames(self):
        total_frames = Game.total_frames()
        found_needed_frames = True
        for x in range(1, total_frames + 1):
            try:
                Frame.objects.get(number=x)
            except Exception:
                found_needed_frames = False
                break
        self.assertEqual(found_needed_frames, True)

    def test_chances(self):
        max_chances = Game.max_chances()
        found_needed_chances = True
        for x in range(1, max_chances + 1):
            try:
                Chance.objects.get(number=x)
            except Exception:
                found_needed_chances = False
                break
        self.assertEqual(found_needed_chances, True)

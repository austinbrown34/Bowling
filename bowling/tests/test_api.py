from django.test import TestCase
from tastypie.test import ResourceTestCaseMixin
from bowling.api.resources import GameManagerResource, PlayerResource, FrameResource, ChanceResource, GameResource, GamePlayerResource, PlayerGameResource
from django.contrib.auth.models import User
from bowling.models import Player, Game, PlayerGame
from bowling.managers import GameManager


class PlayerResourceTest(ResourceTestCaseMixin, TestCase):
    def setUp(self):
        super(PlayerResourceTest, self).setUp()
        self.username = 'testadmin'
        self.password = 'testpass'
        self.user = User.objects.create_user(self.username, 'test@example.com', self.password)
        self.post_data = {
            'name': 'testc',
            'user': {
                'username': 'testuserc',
                'password': '12345'
            }
        }

    def get_apikey(self):
        return self.create_apikey(username=self.username, api_key=self.api_key)

    def get_credentials(self):
        return self.create_basic(username=self.username, password=self.password)

    def test_create_players(self):
        self.assertEqual(Player.objects.count(), 1)
        self.assertHttpOK(
            self.api_client.post(
                '/api/v1/player/create/?username={}&api_key={}'.format(
                    self.user.username, self.user.api_key),
                format='json',
                data=self.post_data,
                authentication=self.get_credentials()
            )
        )
        # Verify a new one has been added.
        self.assertEqual(Player.objects.count(), 2)


class GameManagerResourceTest(ResourceTestCaseMixin, TestCase):
    def setUp(self):
        super(GameManagerResourceTest, self).setUp()
        self.username = 'testadmin'
        self.password = 'testpass'
        self.user = User.objects.create_user(self.username, 'test@example.com', self.password)
        self.api_key = 'test'
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
        self.game = GameManager().new_game(self.player_ids)

    def get_credentials(self):
        return self.create_basic(username=self.username, password=self.password)

    def get_apikey(self):
        return self.create_apikey(username=self.username, api_key=self.api_key)

    def test_gamemanager_new_game(self):
        self.assertEqual(Game.objects.count(), 1)
        self.assertHttpOK(
            self.api_client.get(
                '/api/v1/gamemanager/new_game/?players={},{}&username={}&api_key={}'.format(
                    self.user1.player.id,
                    self.user2.player.id,
                    self.user.username,
                    self.user.api_key
                ),
                authentication=self.get_credentials()
            )
        )
        # Verify a new one has been added.
        self.assertEqual(Game.objects.count(), 2)


class GameResourceTest(ResourceTestCaseMixin, TestCase):
    def setUp(self):
        super(GameResourceTest, self).setUp()
        self.username = 'testadmin'
        self.password = 'testpass'
        self.user = User.objects.create_user(self.username, 'test@example.com', self.password)
        self.api_key = 'test'
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
        self.game = GameManager().new_game(self.player_ids)
        self.game2 = GameManager().new_game(self.player_ids)
        self.game2.start()
        self.game2.bowl('1')
        self.game2.bowl('2')

    def get_credentials(self):
        return self.create_basic(username=self.username, password=self.password)

    def get_apikey(self):
        return self.create_apikey(username=self.username, api_key=self.api_key)

    def test_game_start(self):
        self.assertEqual(self.game.status, 0)
        self.assertHttpOK(
            self.api_client.get(
                '/api/v1/game/{}/start/?username={}&api_key={}'.format(
                    self.game.id,
                    self.user.username,
                    self.user.api_key
                ),
                authentication=self.get_credentials()
            )
        )
        self.assertEqual(self.game.status, 1)

    def test_game_bowl(self):
        self.assertHttpOK(
            self.api_client.get(
                '/api/v1/game/{}/bowl/?mark=1&username={}&api_key={}'.format(
                    self.game.id,
                    self.user.username,
                    self.user.api_key
                ),
                authentication=self.get_credentials()
            )
        )
        gameplayer = self.game.get_gameplayer(self.game.players[0])
        playergame = PlayerGame.objects.get(player=gameplayer)
        self.assertEqual(playergame.mark, 1)

    def test_game_get_state(self):
        resp = self.api_client.get(
            '/api/v1/game/{}/bowl/?mark=1&username={}&api_key={}'.format(
                self.game2.id,
                self.user.username,
                self.user.api_key
            ),
            authentication=self.get_credentials()
        )
        self.assertHttpOK(
            resp
        )
        self.assertValidJSONResponse(resp)
        self.assertEqual(self.deserialize(resp), {"State": {"chance": 1, "frame": 1, "player": "testb", "scores": {"0": {"testa": 3}, "1": {"testb": 0}}}})


class GameResourceTest(ResourceTestCaseMixin, TestCase):
    def setUp(self):
        super(GameManagerResourceTest, self).setUp()

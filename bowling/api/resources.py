from tastypie.resources import ModelResource, ALL_WITH_RELATIONS, ALL, Resource
from tastypie.authentication import ApiKeyAuthentication, MultiAuthentication, SessionAuthentication, BasicAuthentication
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie import fields
from bowling.models import Player, Frame, Chance, Game, PlayerGame, GamePlayer
from django.contrib.auth.models import User
from bowling.managers import GameManager
from django.conf.urls import url
from tastypie.utils import trailing_slash
from tastypie.bundle import Bundle
import json


ALL_METHODS = ['get', 'post', 'put', 'delete', 'patch']


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        allowed_methods = ALL_METHODS
        resource_name = 'user'
        authorization = DjangoAuthorization()
        authentication = MultiAuthentication(
            ApiKeyAuthentication(),
            SessionAuthentication()
        )


class GameManagerResource(Resource):
    class Meta:
        allowed_methods = ['get', 'post']
        resource_name = 'gamemanager'
        authorization = DjangoAuthorization()
        authentication = MultiAuthentication(
            ApiKeyAuthentication(),
            SessionAuthentication(),
            BasicAuthentication()
        )

    def get_object_list(self, request):
        return []

    def obj_get_list(self, request=None, **kwargs):
        return self.get_object_list(request)

    def prepend_urls(self):
        """ Add following array of urls to GameManagerResource base urls """
        return [
            url(r"^(?P<resource_name>%s)/new_game%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('new_game'), name="new_game"),
        ]

    def get_game_resource_uri(self, bundle_or_obj):
        kwargs = {
            'resource_name': 'game',
        }

        if isinstance(bundle_or_obj, Bundle):
            kwargs['pk'] = bundle_or_obj.obj.id
        else:
            kwargs['pk'] = bundle_or_obj.id

        if self._meta.api_name is not None:
            kwargs['api_name'] = self._meta.api_name

        return self._build_reverse_url('api_dispatch_detail', kwargs=kwargs)

    def new_game(self, request, **kwargs):
        self.is_authenticated(request)
        if request.method == 'GET':
            players = request.GET.get('players', '')
        game = GameManager.new_game(players.split(','))
        return self.create_response(
            request,
            {'New Game': self.get_game_resource_uri(game)}
        )


class PlayerResource(ModelResource):
    user = fields.ToOneField(UserResource, 'user', full=True)
    class Meta:
        queryset = Player.objects.all()
        allowed_methods = ALL_METHODS
        resource_name = 'player'
        authorization = DjangoAuthorization()
        authentication = MultiAuthentication(
            ApiKeyAuthentication(),
            SessionAuthentication(),
            BasicAuthentication()
        )
        ordering = {
            'date_created': ALL,
            'date_updated': ALL
        }
        filtering = {
            'id': ALL,
            'name': ALL,
            'date_created': ALL,
            'date_updated': ALL
        }

    def prepend_urls(self):
        """ Add following array of urls to PlayerResource base urls """
        return [
            url(r"^(?P<resource_name>%s)/create%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('create'), name="create")
        ]

    def create(self, request, **kwargs):
        self.is_authenticated(request)
        if request.method == 'POST':
            data = json.loads(request.body)
            user = data['user']
            name = data['name']
        new_user = User.objects.create_user(
            username=user['username'],
            password=user['password']
        )
        new_user.player.name = name
        User.save(new_user)
        return self.create_response(
            request,
            {'New Player': self.get_resource_uri(new_user)}
        )


class FrameResource(ModelResource):
    class Meta:
        queryset = Frame.objects.all()
        allowed_methods = ALL_METHODS
        resource_name = 'frame'
        authorization = DjangoAuthorization()
        authentication = MultiAuthentication(
            ApiKeyAuthentication(),
            SessionAuthentication()
        )
        ordering = {
            'date_created': ALL,
            'date_updated': ALL
        }
        filtering = {
            'id': ALL,
            'number': ALL,
            'date_created': ALL,
            'date_updated': ALL
        }


class ChanceResource(ModelResource):
    class Meta:
        queryset = Chance.objects.all()
        allowed_methods = ALL_METHODS
        resource_name = 'chance'
        authorization = DjangoAuthorization()
        authentication = MultiAuthentication(
            ApiKeyAuthentication(),
            SessionAuthentication()
        )
        ordering = {
            'date_created': ALL,
            'date_updated': ALL
        }
        filtering = {
            'id': ALL,
            'number': ALL,
            'date_created': ALL,
            'date_updated': ALL
        }


class GameResource(ModelResource):
    players = fields.ToManyField(PlayerResource, 'players', null=True, full=True)
    class Meta:
        queryset = Game.objects.all()
        allowed_methods = ALL_METHODS
        resource_name = 'game'
        authorization = DjangoAuthorization()
        authentication = MultiAuthentication(
            ApiKeyAuthentication(),
            SessionAuthentication(),
            BasicAuthentication()
        )
        ordering = {
            'date_created': ALL,
            'date_updated': ALL
        }
        filtering = {
            'id': ALL,
            'players': ALL_WITH_RELATIONS,
            'date_created': ALL,
            'date_updated': ALL
        }

    def prepend_urls(self):
        """ Add following array of urls to GameManagerResource base urls """
        return [
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/start%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('start'), name="start"),
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/bowl%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('bowl'), name="bowl"),
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/get_state%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_state'), name="get_state"),
        ]

    def start(self, request, **kwargs):
        self.is_authenticated(request)
        basic_bundle = self.build_bundle(request=request)
        game = self.cached_obj_get(
            bundle=basic_bundle,
            **self.remove_api_resource_names(kwargs))
        return self.create_response(
            request,
            {"Game Started": game.start()}
        )

    def bowl(self, request, **kwargs):
        if request.method == 'GET':
            mark = request.GET.get('mark', '')
        if request.method == 'POST':
            mark = request.POST.get('mark', '')
        self.is_authenticated(request)
        basic_bundle = self.build_bundle(request=request)
        game = self.cached_obj_get(
            bundle=basic_bundle,
            **self.remove_api_resource_names(kwargs))
        return self.create_response(
            request,
            {"Bowl Entered": game.bowl(mark)}
        )

    def get_state(self, request, **kwargs):
        self.is_authenticated(request)
        basic_bundle = self.build_bundle(request=request)
        game = self.cached_obj_get(
            bundle=basic_bundle,
            **self.remove_api_resource_names(kwargs))
        return self.create_response(
            request,
            {"State": game.get_state()}
        )


class GamePlayerResource(ModelResource):
    player = fields.ForeignKey(PlayerResource, 'player', null=True, full=True)
    game = fields.ForeignKey(GameResource, 'game', null=True, full=True)
    class Meta:
        queryset = GamePlayer.objects.all()
        allowed_methods = ALL_METHODS
        resource_name = 'gameplayer'
        authorization = DjangoAuthorization()
        authentication = MultiAuthentication(
            ApiKeyAuthentication(),
            SessionAuthentication()
        )
        ordering = {
            'date_created': ALL,
            'date_updated': ALL
        }
        filtering = {
            'id': ALL,
            'player': ALL_WITH_RELATIONS,
            'game': ALL_WITH_RELATIONS,
            'date_created': ALL,
            'date_updated': ALL
        }


class PlayerGameResource(ModelResource):
    player = fields.ForeignKey(GamePlayerResource, 'player', null=True, full=True)
    frame = fields.ForeignKey(FrameResource, 'frame', null=True, full=True)
    chance = fields.ForeignKey(ChanceResource, 'chance', null=True, full=True)
    class Meta:
        queryset = PlayerGame.objects.all()
        allowed_methods = ALL_METHODS
        resource_name = 'playergame'
        authorization = DjangoAuthorization()
        authentication = MultiAuthentication(
            ApiKeyAuthentication(),
            SessionAuthentication()
        )
        ordering = {
            'date_created': ALL,
            'date_updated': ALL
        }
        filtering = {
            'player': ALL_WITH_RELATIONS,
            'game': ALL_WITH_RELATIONS,
            'id': ALL,
            'frame': ALL_WITH_RELATIONS,
            'chance': ALL_WITH_RELATIONS,
            'mark': ALL,
            'date_created': ALL,
            'date_updated': ALL
        }

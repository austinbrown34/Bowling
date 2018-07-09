from tastypie.resources import ModelResource, ALL_WITH_RELATIONS, ALL
from tastypie.authentication import ApiKeyAuthentication, MultiAuthentication, SessionAuthentication
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie import fields
from bowling.models import Player, Frame, Chance, Game, PlayerGame, GamePlayer


ALL_METHODS = ['get', 'post', 'put', 'delete', 'patch']


class PlayerResource(ModelResource):
    class Meta:
        queryset = Player.objects.all()
        allowed_methods = ALL_METHODS
        resource_name = 'player'
        authorization = DjangoAuthorization()
        authentication = MultiAuthentication(ApiKeyAuthentication(), SessionAuthentication())
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


class FrameResource(ModelResource):
    class Meta:
        queryset = Frame.objects.all()
        allowed_methods = ALL_METHODS
        resource_name = 'frame'
        authorization = DjangoAuthorization()
        authentication = MultiAuthentication(ApiKeyAuthentication(), SessionAuthentication())
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
        authentication = MultiAuthentication(ApiKeyAuthentication(), SessionAuthentication())
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
        authentication = MultiAuthentication(ApiKeyAuthentication(), SessionAuthentication())
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


class GamePlayerResource(ModelResource):
    player = fields.ForeignKey(PlayerResource, 'player', null=True, full=True)
    game = fields.ForeignKey(GameResource, 'game', null=True, full=True)
    class Meta:
        queryset = GamePlayer.objects.all()
        allowed_methods = ALL_METHODS
        resource_name = 'gameplayer'
        authorization = DjangoAuthorization()
        authentication = MultiAuthentication(ApiKeyAuthentication(), SessionAuthentication())
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
        authentication = MultiAuthentication(ApiKeyAuthentication(), SessionAuthentication())
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

from django.contrib import admin
from bowling.models import Player, Frame, Chance, Game, PlayerGame, GamePlayer


admin.site.register(Player)
admin.site.register(Frame)
admin.site.register(Chance)
admin.site.register(Game)
admin.site.register(PlayerGame)
admin.site.register(GamePlayer)

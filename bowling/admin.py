from django.contrib import admin
from bowling.models import Player, Frame, Chance, Game, PlayerGame


admin.site.register(Player)
admin.site.register(Frame)
admin.site.register(Chance)
admin.site.register(Game)
admin.site.register(PlayerGame)

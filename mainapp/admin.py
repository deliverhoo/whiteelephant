from django.contrib import admin
from .models import Game, Player, Gift, GameProperties
# Register your models here.

admin.site.register(Game)
admin.site.register(Player)
admin.site.register(Gift)
admin.site.register(GameProperties)


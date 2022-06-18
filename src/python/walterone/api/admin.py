from django.contrib import admin

from .models.action import Attack, Defend, Find, Move
from .models.ia import IA
from .models.map import Map
from .models.match import Match, MatchIA
from .models.zone import Zone


class WalterOneSite(admin.AdminSite):
    site_header = 'WalterOne Battle administration'

admin_site = WalterOneSite(name='watcher')
admin_site.register(Attack)
admin_site.register(Defend)
admin_site.register(Find)
admin_site.register(Move)
admin_site.register(IA)
admin_site.register(Map)
admin_site.register(Match)
admin_site.register(MatchIA)
admin_site.register(Zone)

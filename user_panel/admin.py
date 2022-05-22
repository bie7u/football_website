from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(League)
admin.site.register(Season)
admin.site.register(Links)
admin.site.register(Teams)
admin.site.register(TeamProfile)
admin.site.register(Round)
admin.site.register(Matchs)
admin.site.register(ActualMatchs)
admin.site.register(ActualSeason)
admin.site.register(infoAboutRound)
admin.site.register(infoAboutLeague)


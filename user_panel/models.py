from email.policy import default
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.db import models
import datetime


# Admin Panel - 
class League(models.Model):
    league = models.CharField(max_length=200)
    transfer = models.BooleanField(default=False)
    promote_to = models.CharField(max_length=1, blank=True, null=True)
    relegation_to = models.CharField(max_length=1, blank=True, null=True)

    def __str__(self):
        return str(self.league)


class Season(models.Model):
    season = models.CharField(max_length=100)

    def __str__(self):
        return str(self.season)


class Links(models.Model):
    link = models.CharField(max_length=300, blank=True)
    transfer = models.BooleanField(default=False)
    season = models.ForeignKey(Season, default=None, on_delete=CASCADE)
    league = models.ForeignKey(League, default=None, on_delete=CASCADE)
    last_season = models.BooleanField(default=False)

    def __str__(self):
        return f"{str(self.league)} {str(self.season)}"


class Teams(models.Model):
    team = models.CharField(max_length=150)

    def __str__(self):
        return str(self.team)


class TeamProfile(models.Model):
    team = models.ForeignKey(Teams, default=None, on_delete=CASCADE)
    describe = models.TextField(max_length=2000, blank=True)
    arms_of_team = models.ImageField(blank=True, null=True, default='default_arms.png')
    chairman = models.CharField(max_length=30, blank=True, null=True, default='')
    coach = models.CharField(max_length=30, blank=True, null=True, default='')
    colors = models.CharField(max_length=30, blank=True, null=True, default='')
    date_of_creation = models.DateField(default=datetime.date.today())
    capitan = models.CharField(max_length=30, blank=True, null=True, default='')
    stadium = models.CharField(max_length=50, blank=True, null=True, default='')
    publish = models.BooleanField(default=False)
    edit = models.BooleanField(default=False)
    user = models.CharField(blank=True, null=True, max_length=50)
    
    def __str__(self):
        return str(self.team)
        
class Round(models.Model):
    round = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return str(self.round)

class Matchs(models.Model):
    round = models.ForeignKey(Round, default=None, on_delete=CASCADE)
    team_home = models.ForeignKey(Teams, default=None, on_delete=CASCADE, related_name='team_home')
    team_home_result = models.CharField(max_length=10, blank=True)
    team_versus_result = models.CharField(max_length=10, blank=True)
    team_versus = models.ForeignKey(Teams, default=None, on_delete=CASCADE, related_name='team_versus')
    date = models.CharField(max_length=100, blank=True)
    season = models.ForeignKey(Season, default=None, on_delete=CASCADE)
    league = models.ForeignKey(League, default=None, on_delete=CASCADE)
    day = models.DateField(default=datetime.date.today())
    hour = models.TimeField(default=datetime.time)
    match_info = models.TextField(max_length=200, default='')

    def __str__(self):
        return f"{str(self.league)} {str(self.season)} {str(self.team_home)} {str(self.team_versus)}"

class ActualMatchs(models.Model):
    round = models.ForeignKey(Round, default=None, on_delete=CASCADE)
    team_home = models.ForeignKey(Teams, default=None, on_delete=CASCADE, related_name='team_home1')
    team_home_result = models.CharField(max_length=10, blank=True)
    team_versus_result = models.CharField(max_length=10, blank=True)
    team_versus = models.ForeignKey(Teams, default=None, on_delete=CASCADE, related_name='team_versus2')
    date = models.CharField(max_length=100, blank=True)
    season = models.ForeignKey(Season, default=None, on_delete=CASCADE)
    league = models.ForeignKey(League, default=None, on_delete=CASCADE)
    day = models.DateField(default=datetime.date.today())
    hour = models.TimeField(default=datetime.time)
    match_info = models.TextField(max_length=200, default='', blank=True)
    referee = models.CharField(max_length=50, blank=True, null=True, default='Nie podano sędziego')
    active_round = models.BooleanField(default=False)
    finished_round = models.BooleanField(default=False)
    today_match = models.BooleanField(default=False)
    live = models.BooleanField(default=False)
    def __str__(self):
        return f"{str(self.league)} {str(self.season)} {str(self.team_home)} {str(self.team_versus)}"


class ActualSeason(models.Model):
    actual_season = models.CharField(max_length=15)

    def __str__(self):
        return str(self.actual_season)


class infoAboutRound(models.Model):
    league = models.ForeignKey(League, default=None, on_delete=CASCADE)
    round = models.ForeignKey(Round, default=None, on_delete=CASCADE)
    season = models.ForeignKey(ActualSeason, default=None, on_delete=CASCADE)
    info = models.TextField(max_length=200, default='', blank=True)

    def __str__(self):  
        return str(self.league) + ' ' + str(self.round)

class infoAboutLeague(models.Model):
    league = models.ForeignKey(League, default=None, on_delete=CASCADE)
    season = models.ForeignKey(Season, default=None, on_delete=CASCADE)
    info = models.TextField(max_length=200, default='', blank=True)

    def __str__(self):
        return str(self.league) + ' ' + str(self.season)
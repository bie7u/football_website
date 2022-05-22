from django.db import models
from django.forms import BooleanField
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User
from user_panel.models import ActualMatchs, League, Season, Teams

# Create your models here.


class Comment(models.Model):
    user = models.ForeignKey(User, default=None, on_delete=CASCADE)
    match = models.ForeignKey(ActualMatchs, default=None, on_delete=CASCADE)
    comment = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{str(self.user)}, {str(self.created_at)}"


class EditResult(models.Model):
    team_home_sc = models.ForeignKey(Teams, default=None, on_delete=CASCADE, related_name='team_home_sc')
    team_versus_sc = models.ForeignKey(Teams, default=None, on_delete=CASCADE, related_name='team_versus_sc')
    season = models.ForeignKey(Season, default=None, on_delete=CASCADE)
    league = models.ForeignKey(League, default=None, on_delete=CASCADE)
    result_team_home = models.CharField(default=0, max_length=2)
    result_team_versus = models.CharField(default=0, max_length=2)
    time_of_edit = models.DateTimeField(auto_now_add=True)
    accept = models.BooleanField(default=False)
    match = models.ForeignKey(ActualMatchs, default=None, on_delete=CASCADE, related_name='match_sc')

    def __str__(self):
        return f"{self.team_home_sc} - {self.team_versus_sc}"




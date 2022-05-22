from pyexpat import model
from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from ckeditor.fields import RichTextField
from django.shortcuts import get_object_or_404

from user_panel.models import Teams, League
# Create your models here.


class BlogEntry(models.Model):
    types = (
        ('1', 'Artykul sponsorowany'),
        ('2', 'Artykul nie sponsorowany'),
    )


    author = models.ForeignKey(User, default=None, on_delete=CASCADE)
    team = models.ForeignKey(Teams, default=None, on_delete=CASCADE, null=True, blank=True)
    league = models.ForeignKey(League, default=None, on_delete=CASCADE, null=True, blank=True)
    thumbnail = models.ImageField(null=True)
    title = models.CharField(max_length=120, null=True, blank=True)

    entry = RichTextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    admin_agree = models.BooleanField(default=False)
    article_type = models.CharField(max_length=100, choices=types, null=True, default='2')
    publicate_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.author) + ' ' + str(self.title)

class EntryComment(models.Model):
    user = models.ForeignKey(User, default=None, on_delete=CASCADE)
    entry = models.ForeignKey(BlogEntry, default=None, on_delete=CASCADE)
    comment = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user) + ' ' + str(self.entry)


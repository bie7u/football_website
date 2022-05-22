from django.forms import ModelForm
from .models import Comment, EditResult
from django import forms


class CommentForm(ModelForm):
 
    class Meta:
        model = Comment
        fields = '__all__'
        exclude = ['user', 'match']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["comment"].label = ''
        self.fields["comment"].widget.attrs["placeholder"] = "Napisz komentarz...."


class EditResultForm(ModelForm):

    class Meta:
        model = EditResult
        fields = '__all__'
        exclude = ['accept', 'time_of_edit', 'league', 'season', 'team_home_sc', 'team_versus_sc', 'match', 'user']

from django import forms
from .models import BlogEntry, EntryComment


class BlogEntryForm(forms.ModelForm):

    class Meta:
        model = BlogEntry
        fields = ['title', 'entry', 'league', 
                'team', 'thumbnail', 'article_type']
                
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].label = ''
        self.fields["title"].widget.attrs["placeholder"] = "Wpisz tytuł artykułu..."

class EntryCommentForm(forms.ModelForm):

    class Meta:
        model = EntryComment
        fields = ['comment']
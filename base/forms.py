from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = '__all__'
        exclude = ['created_at']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["user_email"].label = ''
        self.fields["user_email"].widget.attrs["placeholder"] = "Podaj email..."
        self.fields["text"].label = ''
        self.fields["text"].widget.attrs["placeholder"] = "Wpisz wiadomość..."
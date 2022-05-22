from hashlib import blake2b
from tokenize import blank_re
from allauth.account.forms import SignupForm, LoginForm, ResetPasswordForm, ResetPasswordKeyForm
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordForm, UserChangeForm

class UserSignUpForm(SignupForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)

    class Meta:
        fields = ("email", "password1", "password2", "first_name")
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].label = ''
        self.fields["email"].widget.attrs["placeholder"] = "Email"
        self.fields["password1"].label = ''
        self.fields["password1"].widget.attrs["placeholder"] = "Hasło..."
        self.fields["password2"].label = ''
        self.fields["password2"].widget.attrs["placeholder"] = "Powtórz hasło..."
        self.fields["first_name"].label = ''
        self.fields["first_name"].widget.attrs["placeholder"] = "Podaj imię..."
        self.fields["last_name"].label = ''
        self.fields["last_name"].widget.attrs["placeholder"] = "Podaj nazwisko..."



class UserLoginForm(LoginForm):

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields["login"].label = ''
        self.fields["login"].widget.attrs["placeholder"] = "Email..."
        self.fields["password"].label = ''
        self.fields["password"].widget.attrs["placeholder"] = "Hasło..."

class UserResetPasswordForm(ResetPasswordForm):

    def __init__(self, *args, **kwargs):
        super(ResetPasswordForm, self).__init__(*args, **kwargs)
        self.fields["email"].label = ''
        self.fields["email"].widget.attrs["placeholder"] = "Email..."

class UserResetPasswordKeyForm(ResetPasswordKeyForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].label = ''
        self.fields["password1"].widget.attrs["placeholder"] = "Nowe hasło..."
        self.fields["password2"].label = ''
        self.fields["password2"].widget.attrs["placeholder"] = "Powtórz hasło..."

class UsernameForm(UserChangeForm):

    class Meta:
        model = get_user_model()
        fields = ('username',)

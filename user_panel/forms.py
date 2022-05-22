from django.forms import DateInput, ModelForm, TimeInput
from .models import Links, League, Matchs, ActualMatchs, Round, TeamProfile, infoAboutLeague, infoAboutRound
from django import forms

class LinksForm(ModelForm):

    class Meta:
        model = Links
        fields = '__all__'
        exclude = ['transfer', 'league', 'last_season',]


class ActualLink(ModelForm):
    link = forms.CharField(max_length=250, widget=forms.TextInput(attrs={'placeholder':'Wklej link...'}))
    class Meta:
        model = Links
        fields = '__all__'
        exclude = ['transfer', 'league', 'last_season', 'season']


class LeagueForm(ModelForm):
    league = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder':'Podaj nazwe ligi...'}))
    class Meta:
        model = League
        fields = '__all__'
        exclude = ['transfer']

class ActualMatchsForm(ModelForm):

    class Meta:
        model = ActualMatchs
        fields = ('match_info',)


# Make Picker
class DatePickerInput(forms.DateInput):
    input_type = 'date'

class TimePickerInput(forms.TimeInput):
    input_type = 'time'
# # # # #


class ActualMatchsSecondForm(ModelForm):
    
    class Meta:
        model = ActualMatchs
        fields = '__all__'
        exclude = ['finished_round', 'active_round', 
        'team_home', 'team_versus', 'season', 'league', 'round', 'live', 'date']
        widgets = {
            'day': DatePickerInput(),
            'hour': TimePickerInput(),
        }

class RoundsForm(ModelForm):

    class Meta:
        model = ActualMatchs
        fields = ('round',)


class infoAboutRoundForm(ModelForm):

    class Meta:
        model = infoAboutRound
        fields = '__all__'
        exclude = ['league', 'round', 'season']


class LeagueFormSecond(ModelForm):
     
    class Meta:
        model = League
        fields = '__all__'
        exclude = ['league', 'transfer']

class infoAboutLeagueForm(ModelForm):

    class Meta:
        model = infoAboutLeague
        fields = '__all__'
        exclude = ['league', 'season']

class TeamProfileForm(ModelForm):

    class Meta:
        model = TeamProfile
        fields = '__all__'
        exclude = ['team']
        widgets = {
            'date_of_creation': DatePickerInput(),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["describe"].label = ''
        self.fields["describe"].widget.attrs["placeholder"] = "Opis drużyny...."
        self.fields["chairman"].label = ''
        self.fields["chairman"].widget.attrs["placeholder"] = "Prezes...."
        self.fields["coach"].label = ''
        self.fields["coach"].widget.attrs["placeholder"] = "Trener...."
        self.fields["colors"].label = ''
        self.fields["colors"].widget.attrs["placeholder"] = "Barwy...."
        self.fields["date_of_creation"].label = ''
        self.fields["date_of_creation"].widget.attrs["placeholder"] = "Data powstania...."
        self.fields["capitan"].label = ''
        self.fields["capitan"].widget.attrs["placeholder"] = "Kapitan drużyny...."
        self.fields["stadium"].label = ''
        self.fields["stadium"].widget.attrs["placeholder"] = "Stadion...."


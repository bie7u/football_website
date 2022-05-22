from django import template
from user_panel.models import TeamProfile, ActualMatchs, League, Teams
from user_panel.models import infoAboutRound

register = template.Library()

@register.filter(name='sequence')
def sequence(value):

    return list(value)


@register.filter(name='zip')
def zip_lists(a, b):

    return zip(a, b)


@register.filter(name='del_')
def del_(value):
    value = str(value)
    value = value.split('_')

    return ' '.join(value)

@register.filter(name='search_league')
def search_league(team):
    if ActualMatchs.objects.filter(team_home=team):
        search_league = ActualMatchs.objects.filter(team_home=team).values_list('league', flat=True).distinct()[0]
        league = League.objects.get(id=search_league)
    else:
        league = 'Drużyna nie gra bądź awansowała na szczebel centralny'

    return league


@register.filter(name='actual__round')
def actual__round(league_id, round_id):
    active_round = ActualMatchs.objects.filter(league=league_id, round=round_id, active_round=True)
    permission = False
    if active_round:
        permission = True
    else: 
        permission = False
    return permission



@register.filter(name='end__round')
def end__round(league_id, round_id):
    finished_round = ActualMatchs.objects.filter(league=league_id, round=round_id, finished_round=True)
    permission = False
    if finished_round:
        permission = True
    else: 
        permission = False
    return permission


@register.filter(name='future__round')
def future__round(league_id, round_id):
    finished_round = ActualMatchs.objects.filter(league=league_id, round=round_id, finished_round=False, active_round=False)
    permission = False
    if finished_round:
        permission = True
    else: 
        permission = False
    return permission

@register.filter(name='transform__match__minute')
def transformMinuteOfMatch(time):
    if time in range(0, 45):
        return f"Na żywo: {time+1}'"
    if time in range(45, 48):
        return f"Na żywo: 45+"
    if time in range(48, 64):
        return 'Przerwa'
    if time in range(64, 109):
        second_half = time- 18
        return f"Na żywo: {second_half}'"
    if time in range(109, 112):
        return f"90+"
    if time > 111:
        return 'Koniec Meczu'

@register.simple_tag
def update_variable(value):
    return value


@register.filter(name='addclass')
def addclass(value, arg):
    return value.as_widget(attrs={'class': arg})


@register.filter(name='round_info')
def round_info(round_id, league_id):
    info = None
    if infoAboutRound.objects.filter(league=league_id, round=round_id):
        info = infoAboutRound.objects.get(league=league_id, round=round_id).info
    return info


@register.filter(name='promotion')
def promotion(value, value_sc):
    if not value_sc:
        return False
    val = False
    if value <= int(value_sc):
        val = True
    return val



@register.filter(name='relegation')
def relegation(value, value_sc):
    if not value_sc:
        return False
    val = False
    if value < int(value_sc):
        val = True
    return val

@register.filter(name='subtraction')
def subtraction(value, value_sc):
    val = value - int(value_sc)
    return val


@register.filter(name='get_group')
def get_group(request):
    return str(request.user.groups.get())





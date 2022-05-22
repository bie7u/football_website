from django.shortcuts import get_object_or_404, redirect, render
from user_panel.forms import ActualMatchsForm
from user_panel.models import ActualMatchs
from datetime import datetime
from datetime import timedelta
from .forms import EditResultForm

# Live Matchs View
def liveMatchs(request):
    live_matches = ActualMatchs.objects.filter(today_match=True)
    
    segregated_live_matches = {}
    for i in live_matches:
        segregated_live_matches[i.league] = []
    for i in live_matches:
        segregated_live_matches[i.league].append(i)
    context = {'live_matches': segregated_live_matches}

    context = {'live_matches': segregated_live_matches}
    return render(request, 'live_matches/live_matchs_page.html', context)


def editLiveMatch(request, team_home_id, team_versus_id):
    match = ActualMatchs.objects.get(live=True, team_home=team_home_id, team_versus=team_versus_id)
    league = match.league
    season = match.season
    team_home = match.team_home
    team_versus = match.team_versus
    form = EditResultForm()
    if request.method == 'POST':
        form = EditResultForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.league = league
            form.season = season
            form.team_home_sc = team_home
            form.team_versus_sc = team_versus
            form.match = match
            form.save()
            return redirect('live-matchs')
            
    context = {'form': form, 'match': match}
    
    return render(request, 'live_matches/edit_live_match.html', context)



# HTMX
def refreshTime(request, id):
    live_match = ActualMatchs.objects.get(id=id)
    current_time = None

    if live_match.live == True:
        now = datetime.now().time()
        t_now = timedelta(hours=now.hour, minutes=now.minute)
        t_match = timedelta(hours=live_match.hour.hour, minutes=live_match.hour.minute)
        t = t_now - t_match
        current_time = int(t.total_seconds()/60)

    context = {'current_time': current_time,  'id':id, 'match': live_match}
    return render(request, 'partials/refresh_match_time.html', context)

def refreshResult(request, id):
    live_match = ActualMatchs.objects.get(id=id)

    context = {'live_match': live_match, 'id':id}
    return render(request, 'partials/refresh_result.html', context)

def editResult(request, id):
    obj = get_object_or_404(ActualMatchs, id=id)
    form = ActualMatchsForm(instance=obj)

    context = {'id': id, 'form': form}
    return render(request, 'partials/edit_result.html', context)



import os
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.shortcuts import render
from .forms import LinksForm, LeagueForm, ActualLink, ActualMatchsSecondForm, TeamProfileForm, infoAboutRoundForm, infoAboutLeagueForm
from .models import ActualMatchs, ActualSeason, League, Links, Round, Season, Matchs, TeamProfile, infoAboutLeague, infoAboutRound
from .decorators import unauthenticated_user, allowed_users
from .scrape import scrape_web
from .script import open_json
from live_matches.models import EditResult
from .tasks import go_background_date
# Create your views here.


@unauthenticated_user
def userHome(request):
    results_to_edit = EditResult.objects.all().order_by('-time_of_edit')
    
    context = {'results_to_edit': results_to_edit}
    return render(request, 'user_panel/user_home.html', context)

@allowed_users(allowed_roles=['admin'])
def adminPanel(request):

    return render(request, 'admin_panel/admin_panel.html')

def deleteJsonFile():
    dir = f"{os.getcwd()}/import_data" 
    all_files = os.listdir(dir)
    all_files.remove('.gitkeep')
    if all_files:
        for f in all_files:
            os.remove(os.path.join(dir, f))

@allowed_users(allowed_roles=['admin'])
def createLeague(request):
    if not League.objects.filter(transfer=False):
        form = LeagueForm
        if request.method == 'POST':
            form = LeagueForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('create_seasons')
    elif League.objects.filter(transfer=False):
        return redirect('create_seasons')

    context = {'form': form}
    return render(request, 'user_panel/admin_panel/create_league.html', context)


@allowed_users(allowed_roles=['admin'])
def createActualSeason(request):
    league = League.objects.get(transfer=False)
    if not Links.objects.filter(league=league, last_season=False):
        form = ActualLink
        if request.method == 'POST':
            form = ActualLink(request.POST)
            if form.is_valid():
                data = form.save(commit=False)
                data.season = Season.objects.get(season=str(ActualSeason.objects.get())) # Info from API- Season.objects.get(season='2021/2022')
                data.league = league
                data.save()
                return redirect('archives_seasons')
    elif Links.objects.get(league=league, last_season=False):
        return redirect('archives_seasons')

    context = {'league': league, 'form': form}
    return render(request, 'user_panel/admin_panel/create_actual_season.html', context)


@allowed_users(allowed_roles=['admin'])
def createArchivesSeasons(request):
    league = League.objects.get(transfer=False)
    added_links  = Links.objects.filter(transfer=False, last_season=True)
    form = LinksForm
    if request.method == 'POST':
        form = LinksForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.league = league
            data.last_season = True
            data.save()

    context = {'league': league, 'form': form, 'added_links': added_links}
    return render(request, 'user_panel/admin_panel/create_archives_seasons.html', context)


@allowed_users(allowed_roles=['admin'])
def summaryCreate(request):
    league = League.objects.get(transfer=False)
    actual_season_link = Links.objects.get(last_season=False, transfer=False)
    archive_season_links = Links.objects.filter(last_season=True, transfer=False)
    
    context = {'league': league, 'actual_season_link': actual_season_link, 
                'archive_season_links': archive_season_links}
    return render(request, 'user_panel/admin_panel/summary_create.html', context)


@allowed_users(allowed_roles=['admin'])
def updateNameLeague(request, id):
    obj = get_object_or_404(League, id=id)
    form = LeagueForm(request.POST or None, instance=obj)
    if request.method == 'POST':
        form = LeagueForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            response = HttpResponse()
            response["HX-Redirect"] = ''
            return response
        else:
            context = {'form':form, 'obj':obj}
            return render(request, 'partials/league_form.html', context)

    context = {"form": form, 'obj': obj}
    return render(request, 'partials/league_form.html', context)


@allowed_users(allowed_roles=['admin'])
def updateActualSeasonLink(request, id):
    obj = get_object_or_404(Links, id=id)
    form = ActualLink(request.POST or None, instance=obj)
    if request.method == 'POST':
        form = ActualLink(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            response = HttpResponse()
            response["HX-Redirect"] = ''
            return response
        else:
            context = {'form':form, 'obj':obj}
            return render(request, 'partials/actual_link_form.html', context)

    context = {'form': form, 'obj': obj}
    return render(request, 'partials/actual_link_form.html', context)


@allowed_users(allowed_roles=['admin'])
def denyCreateSeason(request):
    not_transfer_league = League.objects.filter(transfer=False)
    not_transfer_links = Links.objects.filter(transfer=False)
    if request.method == 'POST':
        not_transfer_league.delete()
        not_transfer_links.delete()
        return redirect('user-home')

    return render(request, 'user_panel/admin_panel/deny_create_season.html')


@allowed_users(allowed_roles=['admin'])
def transfer_archives_data(request):
    deleteJsonFile()
    go_background_date.delay()

    return render(request, 'user_panel/admin_panel/transfer_archives_data.html')


@allowed_users(allowed_roles=['admin', 'editor'])
def editLeague(request):
    leagues = League.objects.filter(transfer=True)

    context = {'leagues': leagues}
    return render(request, 'user_panel/admin_panel/edit_league.html', context)


@allowed_users(allowed_roles=['admin', 'editor'])
def modernLeagueMenu(request, id):
    league = League.objects.get(id=id)
    rounds = ActualMatchs.objects.filter(league=id).values_list('round', flat=True).distinct()
    
    convert_rounds = [Round.objects.get(id=i) for i in rounds]
    convert_rounds = sorted(convert_rounds, key=lambda item: int(str(item.round).split('_')[1]))
    
    context = {'league': league, 'convert_rounds': convert_rounds}
    return render(request, 'user_panel/admin_panel/modern_league_menu.html', context)


@allowed_users(allowed_roles=['admin', 'editor'])
def returnRound(request, league_id, id):
    league_id = league_id
    match_in_round = ActualMatchs.objects.filter(league=league_id, round=id)
    if request.method == 'POST':
        for i in match_in_round:
            i.active_round = False
            i.finished_round = False
            i.save()
        return redirect('modern_league_menu', id=league_id)
    
    context = {'league_id': league_id}
    return render(request, 'admin_panel/return_round.html', context)

@allowed_users(allowed_roles=['admin', 'editor'])
def editRound(request, league_id,  id):
    round = Round.objects.get(id=id)
    league = League.objects.get(id=league_id)
    matchs_in_round = ActualMatchs.objects.filter(league=league_id, round=id)
    
    match_info = infoAboutRound.objects.filter(league=league_id, round=id)

    if match_info:
        form = infoAboutRoundForm(instance=match_info[0])
    else: 
        form = infoAboutRoundForm()
    if request.method == 'POST':

        if match_info:
            form = infoAboutRoundForm(request.POST, instance=match_info[0])
        else: 
            form = infoAboutRoundForm(request.POST)

        if form.is_valid():
            form = form.save(commit=False)
            form.league = League.objects.get(id=league_id)
            form.round = Round.objects.get(id=id)
            form.season = ActualSeason.objects.get()
            form.save()
            return redirect('edit_round', league_id=league_id, id=id)

    context = {'form':form, 'matchs_in_round': matchs_in_round, 'round':round, 'league': league}
    return render(request, 'user_panel/admin_panel/edit_round.html', context)


@allowed_users(allowed_roles=['admin', 'editor'])
def editMatchInRound(request, league_id, round_id, id):
    choose_match_obj = get_object_or_404(ActualMatchs, league=league_id, round=round_id, id=id)
    form = ActualMatchsSecondForm(instance=choose_match_obj)
    if request.method == 'POST':
        form = ActualMatchsSecondForm(request.POST, instance=choose_match_obj)
        if form.is_valid():
            form.save()
            response = HttpResponse()
            response["HX-Redirect"] = ''
            return response
            
    context = {'form': form, 'choose_match_obj': choose_match_obj, 'league_id': league_id, 'round_id': round_id, 'id':id}
    return render(request, 'partials/edit_match.html', context)


@allowed_users(allowed_roles=['admin', 'editor'])
def informationAboutLeague(request, id):
    league_info = League.objects.get(id=id)

    info_about_league = infoAboutLeague.objects.filter(league_id=id, season=Season.objects.get(season=ActualSeason.objects.get().actual_season))
    
    if info_about_league:
        form = infoAboutLeagueForm(instance=info_about_league[0])
    else: 
        form = infoAboutLeagueForm()
    if request.method == 'POST':

        if info_about_league:
            form = infoAboutLeagueForm(request.POST, instance=info_about_league[0])
        else: 
            form = infoAboutLeagueForm(request.POST)

        if form.is_valid():
            form = form.save(commit=False)
            form.season = Season.objects.get(season=ActualSeason.objects.get().actual_season)
            form.league = League.objects.get(id=id)
            form.save()
            return redirect('info_about_league', id=id)
    
    context = {'form': form, 'info_about_league': info_about_league, 'league_info': league_info}
    return render(request, 'user_panel/admin_panel/info_about_league.html', context)


def finishSeason(request, id):
    obj = ActualMatchs.objects.filter(league=id)
    if request.method == 'POST':
        for o in obj:
            Matchs.objects.create(
                round = o.round,
                team_home = o.team_home,
                team_home_result = o.team_home_result,
                team_versus_result = o.team_versus_result,
                team_versus = o.team_versus,
                date = o.date,
                season = o.season,
                league = o.league,
            )

        add_link_to_archive = Links.objects.get(league=id, last_season=False)
        add_link_to_archive.last_season = True
        add_link_to_archive.save()
        obj.delete()
    
    context = {'obj': obj}
    return render(request, 'admin_panel/finish_season.html', context)


def startNewSeason(request, id):
    actual_season = str(ActualSeason.objects.get())
    form = ActualLink
    if request.method == 'POST':
        form = ActualLink(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.season = Season.objects.get(season=actual_season)
            f.league = League.objects.get(id=id)
            f.save()
            scrape_web(f.link, [str(f.league), str(f.season)])
            open_json(table=ActualMatchs)
            deleteJsonFile()

            
    context = {'form': form, 'actual_season': actual_season}
    return render(request, 'admin_panel/start_new_season.html', context)


def editTeamInfo(request, id):
    team = TeamProfile.objects.get(id=id)
    form = TeamProfileForm(instance=team)
    if request.method == 'POST':
        form = TeamProfileForm(request.POST, request.FILES, instance=team)
        if form.is_valid():
            form = form.save(commit=False)
            form.edit = True
            form.user = request.user.email
            form.save()
            return redirect('detail-name', id=id)
    context = {'form': form, 'team': team}
    return render(request, 'user_panel/edit_team_info.html', context)


def manageTeamInfo(request):
    edit_teams = TeamProfile.objects.filter(edit=True)
    
    context = {'edit_teams': edit_teams}
    return render(request, 'user_panel/admin_panel/manage_team_info.html', context)

# HTMX
def deleteLink(reqeust, id):
    obj = get_object_or_404(Links, id=id)
    obj.delete()
    return HttpResponse('')


def setActualRound(request, league_id, id):
    now_a = ActualMatchs.objects.filter(league=league_id, active_round=True)
    for i in now_a:
        i.active_round = False
        i.save()
    future_a = ActualMatchs.objects.filter(league=league_id, round=id)
    for i in future_a:
        i.active_round = True
        i.finished_round = False
        i.save()
    response = HttpResponse()
    response["HX-Redirect"] = ''
    return response


def setFinishRound(request, league_id, id):
    now_a = ActualMatchs.objects.filter(league=league_id, round=id)
    for i in now_a:
        i.finished_round = True
        i.active_round = False
        i.save()
    response = HttpResponse()
    response["HX-Redirect"] = ''
    return response

def setFutureRound(request, league_id, id):
    now_a = ActualMatchs.objects.filter(league=league_id, round=id)
    for i in now_a:
        i.finished_round = False
        i.active_round = False
        i.save()
    response = HttpResponse()
    response["HX-Redirect"] = ''
    return response


def updateTeamInfo(request, id):
    team = TeamProfile.objects.get(id=id)
    team.edit = False
    team.publish = True
    team.save()
    response = HttpResponse()
    response["HX-Redirect"] = ''
    return response


def actualMatchResult(request, match_id, result_id):
    result = EditResult.objects.get(id=result_id)
    match = ActualMatchs.objects.get(id=match_id)

    match.team_home_result = str(result.result_team_home)
    match.team_versus_result = str(result.result_team_versus)
    match.save()
    result.delete()
    response = HttpResponse()
    response["HX-Redirect"] = ''
    return response

def denyMatchResult(request, result_id):
    result = EditResult.objects.get(id=result_id)
    result.delete()
    response = HttpResponse()
    response["HX-Redirect"] = ''
    return response

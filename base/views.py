from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from itertools import chain
from django.db.models import Q
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from user_panel.models import ActualMatchs, ActualSeason, League, Teams, TeamProfile, Matchs
from live_matches.forms import CommentForm
from live_matches.models import Comment
from blog.models import BlogEntry
from user_panel.models import Season, infoAboutLeague
from user_panel.forms import infoAboutLeagueForm
from .forms import ContactForm


def search_direct_matches(match):
    matchs_archive = Matchs.objects.filter(Q(team_home=match.team_home) | Q(team_home=match.team_versus), Q(team_versus=match.team_home) | Q(team_versus=match.team_versus))
    matchs_actually = ActualMatchs.objects.filter(Q(team_home=match.team_home) | Q(team_home=match.team_versus), Q(team_versus=match.team_home) | Q(team_versus=match.team_versus))
    result = list(chain(matchs_archive, matchs_actually))
    direct_matches = sorted(result, key=lambda instance: instance.season.id)
    return direct_matches


def last_five_matches(team):
    all_finished_matches = ActualMatchs.objects.filter(Q(team_home=team) | Q(team_versus=team)).exclude(team_home_result='')
    all_finished_matches = sorted(all_finished_matches, key=lambda instance: instance.day, reverse=True)
    five_matches = None
    if len(all_finished_matches) == 0:
        return five_matches
    if len(all_finished_matches) < 5:
        five_matches = all_finished_matches[:len(all_finished_matches)]
    elif len(all_finished_matches) >= 5:
        five_matches = all_finished_matches[:5]

    return five_matches

def formGraph(team, last_five_matches):
    result = []
    if last_five_matches:
        for i in last_five_matches:
            if i.team_home == team:
                if i.team_home_result > i.team_versus_result:
                    result.append('Z')
                elif i.team_home_result < i.team_versus_result:
                    result.append('P')
                elif i.team_home_result == i.team_versus_result:
                    result.append('R')
            if i.team_versus == team:
                if i.team_home_result < i.team_versus_result:
                    result.append('Z')
                elif i.team_home_result > i.team_versus_result:
                    result.append('P')
                elif i.team_home_result == i.team_versus_result:
                    result.append('R')
    return result

def showTable(obj, archive=False):

    # Order of teams
    def addOrder(table):
        teams = list(table.keys())
        ready_table = []
        for i in zip(table.items(), range(1, len(teams)+1)):
            ready_table.append(i)
        return ready_table

    # Add actual round 
    def actualRound(table):
        a_table = None
        for i in table.keys():
            league = ActualMatchs.objects.filter(team_home=i).values_list('league', flat=True).distinct()[0]
            actual_round = ActualMatchs.objects.filter(league=league, active_round=True)
            a_table = actual_round
            break
        return a_table

    table = {}
    for data in obj:
        round = data.round

        team_home = data.team_home
        if team_home not in list(table.keys()):
            table[team_home] = [{'punkty': 0, 'zwyciestwa': 0, 'remisy': 0, 'porażki': 0, 
            'bramki strzelone': 0, 'bramki stracone': 0, 'rozegrane mecze': 0}]

        team_home_result = data.team_home_result
        team_versus_result = data.team_versus_result
        team_versus = data.team_versus

        if team_versus not in list(table.keys()):
            table[team_versus] = [{'punkty': 0, 'zwyciestwa': 0, 'remisy': 0, 'porażki': 0, 
            'bramki strzelone': 0, 'bramki stracone': 0, 'rozegrane mecze': 0}]
        if (team_home_result or team_versus_result) == '':
            continue
        
        if int(team_home_result) > int(team_versus_result):
            table[team_home][0]['rozegrane mecze'] += 1
            table[team_versus][0]['rozegrane mecze'] += 1

            table[team_home][0]['punkty'] +=3
            table[team_home][0]['zwyciestwa'] +=1
            table[team_versus][0]['porażki'] +=1

            table[team_home][0]['bramki strzelone'] += int(team_home_result)
            table[team_home][0]['bramki stracone'] += int(team_versus_result)

            table[team_versus][0]['bramki strzelone'] += int(team_versus_result)
            table[team_versus][0]['bramki stracone'] += int(team_home_result)
            continue

        if int(team_home_result) < int(team_versus_result):
            table[team_home][0]['rozegrane mecze'] += 1
            table[team_versus][0]['rozegrane mecze'] += 1

            table[team_versus][0]['punkty'] +=3
            table[team_home][0]['porażki'] +=1
            table[team_versus][0]['zwyciestwa'] +=1

            table[team_home][0]['bramki strzelone'] += int(team_home_result)
            table[team_home][0]['bramki stracone'] += int(team_versus_result)

            table[team_versus][0]['bramki strzelone'] += int(team_versus_result)
            table[team_versus][0]['bramki stracone'] += int(team_home_result)
            continue

        if int(team_home_result) == int(team_versus_result):
            table[team_home][0]['rozegrane mecze'] += 1
            table[team_versus][0]['rozegrane mecze'] += 1

            table[team_home][0]['punkty'] +=1
            table[team_versus][0]['punkty'] +=1
            table[team_home][0]['remisy'] +=1
            table[team_versus][0]['remisy'] +=1

            table[team_home][0]['bramki strzelone'] += int(team_home_result)
            table[team_home][0]['bramki stracone'] += int(team_versus_result)

            table[team_versus][0]['bramki strzelone'] += int(team_versus_result)
            table[team_versus][0]['bramki stracone'] += int(team_home_result)
            continue

    # transform table 
    solo_table = dict(sorted(table.items(), key=lambda item: item[1][0].get('punkty'),  reverse=True))
    if archive == False:
        table = [addOrder(solo_table), actualRound(solo_table)]
    if archive == True:
        table = [addOrder(solo_table), None]
    return table


def makeTimetable(obj):
    round = None
    timetable = {}
    round_matchs = []
    # for match in sorted(obj, key=lambda item: int(str(item.round).split('_')[1])):
    for match in obj:
        if match.round != round:
            if round != None:
                timetable[round] = round_matchs
            round = match.round
            round_matchs = []
        round_matchs.append(match)
    timetable[round] = round_matchs

    return timetable


def get_last_team_seasons(team):
    archive_seasons = Matchs.objects.filter(team_home=team)
    last_seasons = {}
    for i in archive_seasons:
        if i.season not in list(last_seasons.keys()):
            last_seasons[i.season] = i.league

    return last_seasons


# Views


# Home Page
def homePage(request):
    leagues = League.objects.all()
    try:
        latest_sponsor_article = list(BlogEntry.objects.filter(article_type='1', admin_agree=True).order_by('-publicate_at'))[0]
    except:
        latest_sponsor_article = None
    try:
        sponsor_articles = list(BlogEntry.objects.filter(article_type='1', admin_agree=True).order_by('-publicate_at'))[1:5]
    except:
        sponsor_articles = None

    context = {'leagues': leagues, 'sponsor_articles': sponsor_articles, 'latest_sponsor_article': latest_sponsor_article}
    return render(request, 'base/home_page.html', context)

# HTMX show league
def showLeagueTable(request, id):
    league = League.objects.get(id=id)
    table = showTable(obj=ActualMatchs.objects.filter(league=id))
    finish_table = {}
    finish_table[league] = table

    context = {'finish_table': finish_table}
    return render(request, 'partials/show_league_table.html', context)

# Teams Page
def teamsPage(request):
    teams = TeamProfile.objects.all().order_by('team__team') # Double underlines needed to go to foreignkey value string

    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(teams, 15)
    try:
        teams_pag = paginator.page(page) 
    except PageNotAnInteger:
        teams_pag = paginator.page(1)
    except EmptyPage:
        teams_pag = paginator.page(paginator.num_pages)

    context = {'teams_pag': teams_pag}
    return render(request, 'base/teams_page.html', context)

# Detail about match
def detailMatch(request, id):
    match = ActualMatchs.objects.get(id=id)
    direct_matches = search_direct_matches(match)
    team_home = match.team_home
    team_versus = match.team_versus
    last_five_team_home_matches = last_five_matches(team_home)
    last_five_team_versus_matches = last_five_matches(team_versus)
    team_home_form_graph = formGraph(team_home, last_five_team_home_matches)
    team_versus_form_graph = formGraph(team_versus, last_five_team_versus_matches)

    team_home_profile = TeamProfile.objects.get(team__team=match.team_home)
    team_versus_profile = TeamProfile.objects.get(team__team=match.team_versus)
    stadium = TeamProfile.objects.get(team=team_home).stadium
    
    # Add comments 
    comment = CommentForm
    if request.method == 'POST':
        comment = CommentForm(request.POST)
        if comment.is_valid():
            comment = comment.save(commit=False)
            comment.user = request.user
            comment.match = match
            comment.save()
            return redirect('detail_match', id)
       
    all_comments = Comment.objects.filter(match_id=id)
    
    context = {'match': match, 'direct_matches': direct_matches, 
               'last_five_team_home_matches': last_five_team_home_matches,
               'last_five_team_versus_matches': last_five_team_versus_matches,
               'team_home_form_graph': team_home_form_graph,
               'team_versus_form_graph': team_versus_form_graph,
               'team_home_profile': team_home_profile,
               'team_versus_profile': team_versus_profile,
               'comment': comment,
               'all_comments': all_comments,
               'stadium': stadium,
               }
    return render(request, 'base/detail_match.html', context)


# HTMX search
def searchTeam(request):
    search_text = request.POST.get('search')
    results = None
    if search_text:
        results = TeamProfile.objects.filter(team__team__icontains=search_text)[:10]
    context = {'results': results}
    return render(request, 'partials/search-result.html', context)

# Detail about team
def detailTeam(request, id):
    team = Teams.objects.get(id=id)
    team_profile = TeamProfile.objects.get(team__team=team)
    team_id = team_profile.id

    # if someone not edited team info
    if not team_profile.publish == True:
       team_profile = None 

    current_league = None
    last_seasons = get_last_team_seasons(team)

    try:
        current_league = League.objects.get(id=ActualMatchs.objects.filter(team_home=team).values_list('league', flat=True)[0])
    except:
        current_league = None
    
    context = {'team_profile': team_profile, 'current_league': current_league, 'last_seasons': last_seasons, 'team_id': team_id, 'team': team}
    return render(request, 'base/detail_team.html', context)


# Leagues View
def chooseLeague(request):
    leagues = League.objects.all()

    context = {'leagues': leagues}    
    return render(request, 'base/choose_league.html', context)


def showLeague(request, id):
    current_league = ActualMatchs.objects.filter(league=id)
    time_table = makeTimetable(current_league)

    try:
        info_about_league = infoAboutLeague.objects.get(league=id, season__season=str(ActualSeason.objects.get()))
    except:
        info_about_league = None
    
    # Add league to table
    tables = {}
    tables[League.objects.get(id=id)] = (showTable(obj=current_league))


    context = {'tables': tables, 'time_table': time_table, 'info_about_league': info_about_league}
    return render(request, 'base/show_league.html', context)





# Archive views

def archiveSeasons(request):
    obj = League.objects.filter(transfer=True)
    context = {'obj': obj}
    return render(request, 'base/archive_seasons.html', context)


def archiveSeasonsLeague(request, id):
    seasons = sorted(list(Matchs.objects.filter(league=id).values_list('season', flat=True).distinct())) # Get only seasons which have archive
    archive_seasons = [Season.objects.get(id=season) for season in seasons]
    context = {'archive_seasons': archive_seasons, 'id':id}
    return render(request, 'base/archive_seasons_league.html', context)


def particularArchiveSeason(requets, id,  season):
    season = Season.objects.get(id=season)
    league = League.objects.get(id=id)
    current_league = Matchs.objects.filter(season=season, league=id)
    time_table = makeTimetable(current_league)


    try:
        info_about_league = infoAboutLeague.objects.get(league=id, season=season)
    except:
        info_about_league = None

    # Add league to table
    tables = {}
    tables[League.objects.get(id=id)] = (showTable(obj=current_league, archive=True))

    context = { 'tables': tables, 'time_table': time_table, 'season': season, 
        'info_about_league': info_about_league, 'league':league}
    return render(requets, 'base/particular_archive_season.html', context)


def contactView(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            email = form.user_email
            text = form.text
            send_mail(
                subject='Email Kontaktowy',
                message=text,
                from_email=email,
                recipient_list=[settings.EMAIL_HOST_USER],
            )
            messages.success(request, 'Wiadomość została wysłana')
            return redirect('contact-form')
    context = {'form': form}
    return render(request, 'base/contact_form.html', context)

# HTMX

def addArchiveSeasonInfo(request, league, season):
    try:
        obj = get_object_or_404(infoAboutLeague, league=league, season=season)
    except:
        obj = None

    if obj:
        form = infoAboutLeagueForm(instance=obj)
    else: 
        form = infoAboutLeagueForm(request.POST)
    
    if request.method == 'POST':
        if obj:
            form = infoAboutLeagueForm(request.POST, instance=obj)
        else: 
            form = infoAboutLeagueForm(request.POST)
        
        if form.is_valid():
            form = form.save(commit=False)
            form.league = League.objects.get(id=league)
            form.season = Season.objects.get(id=season)
            form.save()
            response = HttpResponse()
            response["HX-Redirect"] = ''
            return response
    context = {'form': form, 'league': league, 'season': season}
    return render(request, 'partials/add_archive_season_info.html', context)
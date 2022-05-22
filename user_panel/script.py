import datetime
import os
import json
from .models import League, Season, Teams, Matchs, Round, TeamProfile



def open_json( table):
    cwd = os.getcwd() # Actual path
    update = f"{cwd}/import_data" # JSON paths
    all_files = os.listdir(update)
    all_files.remove('.gitkeep')
    
    for file in all_files:
        
        with open(f"import_data/{file}", 'r', encoding='utf-8') as fh:
            
            library = json.load(fh)
        transform_data(library, table)



def create_team_team_profile(team):
    Teams.objects.create(
        team = team)
    TeamProfile.objects.create(
        team=Teams.objects.get(team=team))





def transform_date(match_date, season):
    year = 2000
    months = {
        'stycznia': 1,
        'lutego': 2,
        'marca': 3,
        'kwietnia': 4,
        'maja': 5,
        'czerwca': 6,
        'lipca': 7,
        'sierpnia': 8,
        'września': 9,
        'października': 10,
        'listopada': 11,
        'grudnia': 12,
    }
    second_part = [1, 2, 3, 4, 5, 6]
    first_part = [7, 8, 9, 10, 11, 12]
    if match_date:
        date = match_date.split()

        day = date[0]

        if '-' in [i for i in day]:
            day = 1
        else:
            day = int(date[0])
        if date[1][-1] == ',':
            month = months.get(date[1][:-1])
        else:
            month = months.get(date[1])

        if month in first_part:
            year = int(season[:4])
        elif month in second_part:
            year = int(season[5:])
        if len(date) > 2:
            time = date[2].split(':')
            hour = int(time[0])
            minutes = int(time[1])
            return [day, month, year, hour, minutes]
        else:
            return [day, month, year, 0, 0]
    else:
        return [1, 1, 2000, 0, 0]

def transform_data(library, table):
    teams = library[0]
    league = library[2][0]
    season = library[2][1]
    data_teams = Teams.objects.all()
    data_teams = list(data_teams.values_list('team', flat=True))
    for team in teams:
        if team not in data_teams:
            create_team_team_profile(team)
    match_data_o = Matchs.objects.all()
    all_matches = []
    for match in match_data_o:
        all_matches.append(str(match))
    # match scrap 
    for i, x in library[1].items():
        round = '_'.join(i.split()[:2])
        data_round = Round.objects.all()
        data_round = list(data_round.values_list('round', flat=True))
        if round not in data_round:
            Round.objects.create(
                round = round
            )
        for n in x:
            result_team = '' 
            result_team_versus = ''
            keys = list(n[0].keys())
            values = list(n[0].values())
            team = keys[0]
            team_versus = keys[1]
            if values[0]:
                result_team = int(values[0])
            if values[1]:
                result_team_versus = int(values[1])
            match_date = values[2]
            if not team in list(Teams.objects.all().values_list('team', flat=True)):
                create_team_team_profile(team)
            if not team_versus in list(Teams.objects.all().values_list('team', flat=True)):
                create_team_team_profile(team_versus)

            actuall_match = f"{league} {season} {team} {team_versus}"
            d = transform_date(match_date, season)
            match_day = datetime.date(d[2], d[1], d[0])
            match_hour = datetime.time(d[3], d[4])

            if actuall_match not in all_matches:
                table.objects.create(
                    round = Round.objects.get(round=round),
                    team_home = Teams.objects.get(team=team),
                    team_home_result = result_team,
                    team_versus_result = result_team_versus,
                    team_versus = Teams.objects.get(team=team_versus),
                    date = match_date,
                    season = Season.objects.get(season=season),
                    league = League.objects.get(league=league),
                    day = match_day,
                    hour = match_hour,
                )

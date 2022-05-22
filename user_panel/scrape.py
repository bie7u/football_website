from bs4 import BeautifulSoup
import requests
import json
from .models import Links
import os


def scrape_teams(soup):

    teams = []
    condition = {'align': 'left', 'valign': 'middle'}

    for child in soup.find_all('tr'):
        if child.find_all('td', attrs=condition):
            if child.find('td', attrs=condition).get_text().strip() in teams:
                continue
            teams.append(child.find('td', attrs=condition).get_text().strip())

    return teams


def scrape_timetable(soup, teams):

    round = None
    all_matches = {}

    for child in soup.find_all('tr'):
        teams = child.find_all('td', attrs={'nowrap': "", 'valign': "top", "width": "180"})
        results = child.find('td', attrs={'align': 'center', 'nowrap': '', 'valign': 'top', 'width': '50'})
        time = child.find('td', attrs={'valign': 'top', 'width': '190'})

        if child.find('u'):
            if not 'Pauza' in child.find('u').get_text().strip():
                round = child.find('u').get_text().strip()
                all_matches.setdefault(round, [])


        if teams:
            res = results.get_text().strip().split('-')
            date = time.get_text().strip()
            team_1 = teams[0].get_text().strip()
            team_2 = teams[1].get_text().strip()
            b = [{team_1: res[0], team_2: res[1], 'Data': date}]
            if b not in all_matches[round]:
                all_matches[round].append(b)
    return all_matches


def scrape_web(link, name):
    page = requests.get(link)
    page.encoding = 'UTF-8'
    soup = BeautifulSoup(page.content, 'html.parser')
    for i in Links.objects.filter(link=link):
        i.transfer = True
        i.save()
    teams = scrape_teams(soup)
    time_table = scrape_timetable(soup, teams)


    full_data = [teams, time_table, name]

    season = ' '.join(name[1].split('/'))
    with open(f'import_data/{name[0]} {season}.json', 'w', encoding='utf8') as json_file:
        json.dump(full_data, json_file, ensure_ascii=False, indent=4)
    print(f"Dane {name[0]} {name[1]} zostaly przechwycone")



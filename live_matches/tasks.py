# weather/tasks.py
import requests

from django.conf import settings
from celery import shared_task

import live_matches
from user_panel.models import ActualMatchs
from celery.schedules import crontab
from datetime import date, datetime
from datetime import timedelta


@shared_task
def setTodayMatches():
    last_matches = ActualMatchs.objects.filter(today_match=True)
    for match in last_matches:
        match.today_match = False
        match.save()
    today_matchs = ActualMatchs.objects.filter(day=date.today())
    for match in today_matchs:
        match.today_match = True
        match.save()


@shared_task
def setLiveMatch():
    now_time = datetime.now()
    now_hour = now_time.hour
    now_minute = now_time.minute
    live_matches = ActualMatchs.objects.filter(today_match=True, live=False)
    for i in live_matches:
        match_hour = i.hour.hour
        match_minute = i.hour.minute
        if match_hour == now_hour and match_minute == now_minute:
            i.team_home_result = '0'
            i.team_versus_result = '0'
            i.live = True
            i.save()

@shared_task
def delLiveMatch():
    live_matches = ActualMatchs.objects.filter(live=True)
    now = datetime.now().time()
    t_now = timedelta(hours=now.hour, minutes=now.minute)

    for match in live_matches:
        t_match = timedelta(hours=match.hour.hour, minutes=match.hour.minute)
        t = t_now - t_match

        convert_to_minute = a = t.total_seconds()/60

        if convert_to_minute > 130:
            match.live = False
            match.save()

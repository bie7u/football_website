
from celery import Celery
import os
import django
from celery.schedules import crontab
from django.conf import settings
from django.apps import apps
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_app.settings')
django.setup()


app = Celery('web_app')
# namespace='CELERY' means all celery-related configuration keys
# should be uppercased and have a `CELERY_` prefix in Django settings.
# https://docs.celeryproject.org/en/stable/userguide/configuration.html
app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.timezone = 'Europe/Warsaw'
app.conf.enable_utc = True

app.conf.beat_schedule = {
    'every-day': {
        'task': 'live_matches.tasks.setTodayMatches',
        'schedule':  crontab(hour=0, minute=1)},  #  Everyday set today matches at 0:01 AM
    'every-minute': {
        'task': 'live_matches.tasks.setLiveMatch',
        'schedule': 60},
    'every-minute-two': {
        'task': 'live_matches.tasks.delLiveMatch',
        'schedule': 60}
    }

# When we use the following in Django, it loads all the <appname>.tasks
# files and registers any tasks it finds in them. We can import the
# tasks files some other way if we prefer.
app.autodiscover_tasks(lambda: [n.name for n in apps.get_app_configs()])


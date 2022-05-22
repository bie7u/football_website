from celery import shared_task
import os
from .models import ActualMatchs, League, Links, Matchs
from .scrape import scrape_web
from .script import open_json

def deleteJsonFile():
    dir = f"{os.getcwd()}/import_data" 
    all_files = os.listdir(dir)
    all_files.remove('.gitkeep')
    if all_files:
        for f in all_files:
            os.remove(os.path.join(dir, f))


@shared_task(bind=True)
def go_background_date(self):

    link_archive = Links.objects.filter(transfer=False, last_season=True)
    for link in link_archive:
        scrape_web(link.link, [str(link.league), str(link.season)])
        open_json(table=Matchs)
        
    link_archive = Links.objects.filter(transfer=False, last_season=False)
    for link in link_archive:
        scrape_web(link.link, [str(link.league), str(link.season)])
        open_json(table=ActualMatchs)

    # Delete JSON files 
    deleteJsonFile()

    league_active = League.objects.get(transfer=False)
    league_active.transfer = True
    league_active.save()
    return 'Done'
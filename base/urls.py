from django.urls import path
from .import views


urlpatterns = [
    path('', views.homePage, name='home-page'),
    path('druzyny/', views.teamsPage, name='teams-page'),
    path('wyszukaj_druzyne/', views.searchTeam, name='search-team'),
    path('drużyny/<int:id>', views.detailTeam, name='detail-name'),
    path('wybierz_lige/', views.chooseLeague, name='choose-league'),
    path('wybierz_lige/<int:id>', views.showLeague, name='show_league'),
    path('szczegóły_meczu/<int:id>', views.detailMatch, name='detail_match'),
    path('archiwum/', views.archiveSeasons, name='archive_seasons'),
    path('archiwum/sezon/<int:id>', views.archiveSeasonsLeague, name='archive_seasons_league'),
    path('archiwum/sezon/<int:id>/<int:season>', views.particularArchiveSeason, name='particular_archive_season'),
    path('kontakt/', views.contactView, name='contact-form'),

    # HTMX
    path('show_league_table/<int:id>', views.showLeagueTable, name='show-league-table'),
    path('dodaj_archiwalny_opis/<int:league>/<int:season>/', views.addArchiveSeasonInfo, name='add-archive-info')
]
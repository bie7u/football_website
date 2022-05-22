from django.urls import path
from .import views


urlpatterns = [
    path('menu_użytkownika/', views.userHome, name="user-home"),
    path('admin_panel/', views.adminPanel, name='admin_panel'),
    path('admin_panel/stworz_lige/', views.createLeague, name='create_league'),
    path('admin_panel/stworz_lige/dodaj_aktualny_sezon/', views.createActualSeason, name='create_seasons'),
    path('admin_panel/stworz_lige/dodaj_archiwalne_sezony/', views.createArchivesSeasons, name='archives_seasons'),
    path('admin_panel/stworz_lige/podsumowanie/', views.summaryCreate, name='summary_create'),
    path('admin_panel/stworz_lige/anuluj_dodawanie_ligi/', views.denyCreateSeason, name='deny_create'),
    path('admin_panel/pobieranie_danych/', views.transfer_archives_data, name='transfer_archives_seasons'),

    path('admin_panel/edytuj_lige/', views.editLeague, name='edit_league'),
    path('admin_panel/edytuj_lige/menu/<int:id>/', views.modernLeagueMenu, name='modern_league_menu'),
    path('admin_panel/modern_league/<int:id>/finish_season/', views.finishSeason, name='finish_season'),
    path('admin_panel/modern_league/<int:id>/start_new_season/', views.startNewSeason, name='start_new_season'),
    path('admin_panel/modern_league/<int:id>/information/', views.informationAboutLeague, name='info_about_league'),
    path('admin_panel/modern_league/<int:league_id>/<int:id>/return_round/', views.returnRound, name='return_round'),
    path('admin_panel/edytuj_lige/<int:league_id>/<int:id>/edytuj_kolejke', views.editRound, name='edit_round'),
    path('edytuj_druzyne/<int:id>', views.editTeamInfo, name='edit-team-info'),
    path('admin_panel/zarzadzaj_druzynami/', views.manageTeamInfo, name='manage-teams'),

    # HTMX
    path('htmx/delete/<id>/', views.deleteLink, name='delete-link'),
    path('htmx/update/<id>', views.updateNameLeague, name='update-name-league'),
    path('htmx/update_link/<id>', views.updateActualSeasonLink, name='update-actual-season-link'),
    path('htmx/set_actual_round/<league_id>/<id>/', views.setActualRound, name='set-actual-round'),
    path('htmx/set_finish_round/<league_id>/<id>/', views.setFinishRound, name='set-finish-round'),
    path('htmx/set_future_round/<league_id>/<id>/', views.setFutureRound, name='set-future-round'),
    path('htmx/<int:league_id>/<int:round_id>/<int:id>/edit_round_match', views.editMatchInRound, name='edit_round_match'),
    path('htmx/update_team_info/<int:id>', views.updateTeamInfo, name='update-team-info'),
    path('htmx/edit_result/<int:match_id>/<int:result_id>/', views.actualMatchResult, name='actual-match-result'),
    path('htmx/deny_result/<int:result_id>/', views.denyMatchResult, name='deny-match-result'),

]
from django.urls import path, re_path
from .import views, messenger_set

urlpatterns = [
    path('mecze_na_żywo/', views.liveMatchs, name='live-matchs'),
    path('edit_live/<team_home_id>/<team_versus_id>/', views.editLiveMatch, name='edit-live-match'),

    # HTMX
    path('refresh_time/<int:id>', views.refreshTime, name='refresh-time'),
    path('refresh_result/<int:id>', views.refreshResult, name='refresh-result'),
    path('edit_result/<int:id>', views.editResult, name='edit-result'),

    re_path(r'^***/?$', messenger_set.YoMamaBotView.as_view()), # Personal link from Facebook API

]

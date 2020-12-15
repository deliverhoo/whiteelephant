from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    #home page
    path('', views.index),
    path('game/<int:game_id>', views.game_page),
    path('summary/<int:game_id>', views.summary_page),

    #REST APIs below
    #get pages
    path('games/', views.games_list),
    path('players/<int:game_id>', views.get_all_players),
    path('current_player/<int:game_id>', views.get_current_player),
    path('unopened_gifts/<int:game_id>', views.get_unopened_gifts),
    path('all_gifts/<int:game_id>', views.get_all_gifts),
    path('game_properties/<int:game_id>', views.get_game_properties),

    #post methods, disgused as get
    path('start_game/<int:game_id>', views.start_game),
    path('reset_game/<int:game_id>', views.reset_game),
    path('open_gift/<int:game_id>/<int:gift_id>', views.open_gift),
    path('steal_gift/<int:game_id>/<int:gift_id>', views.steal_gift),
    path('keep_gift/<int:game_id>', views.keep_gift),
]

urlpatterns = format_suffix_patterns(urlpatterns)

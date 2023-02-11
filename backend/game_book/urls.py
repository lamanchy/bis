from django.urls import path

from game_book.views import GameBookView, NewGameView, EditGameView, GameView

urlpatterns = [
    path("", GameBookView.as_view(), name="game_book"),
    path("new_game/", NewGameView.as_view(), name="new_game"),
    path("game/<int:pk>/", GameView.as_view(), name="game"),
    path("game/<int:pk>/edit/", EditGameView.as_view(), name="edit_game"),
]

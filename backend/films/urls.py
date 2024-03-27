from django.urls import path

from .views import FilmView

urlpatterns = [
    path("", FilmView.as_view(actions={"get": "list"})),
    path("<str:imdb_id>", FilmView.as_view(actions={"get": "retrieve"})),
]

from django.urls import path

from .views import FilmView

urlpatterns = [
    path("", FilmView.as_view(actions={"get": "list"})),
    path("search/", FilmView.as_view(actions={"get": "search"})),
    path("<str:film_id>/", FilmView.as_view(actions={"get": "retrieve"})),
]

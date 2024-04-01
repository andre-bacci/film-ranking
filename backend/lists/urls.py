from django.urls import path

from .views import CompilationView, ListView, RankingView

urlpatterns = [
    path(
        "compilations/",
        CompilationView.as_view(actions={"get": "list", "post": "create"}),
    ),
    path(
        "compilations/<str:pk>/",
        CompilationView.as_view(actions={"get": "retrieve", "delete": "destroy"}),
    ),
    path(
        "compilations/<str:pk>/calculate_ranking/",
        CompilationView.as_view(actions={"patch": "calculate_ranking"}),
    ),
    path(
        "rankings/",
        RankingView.as_view(actions={"get": "list"}),
    ),
    path(
        "rankings/<str:pk>/",
        RankingView.as_view(actions={"get": "retrieve", "delete": "destroy"}),
    ),
    path(
        "individual_lists/",
        ListView.as_view(actions={"get": "list", "post": "create"}),
    ),
    path(
        "individual_lists/<str:pk>/",
        ListView.as_view(actions={"get": "retrieve", "delete": "destroy"}),
    ),
]

from django.urls import path

from .views import CompilationView, ListView

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
        "<str:compilation_id>/",
        ListView.as_view(actions={"get": "list", "post": "create"}),
    ),
    path(
        "<str:compilation_id>/<str:pk>/",
        ListView.as_view(actions={"get": "retrieve", "delete": "destroy"}),
    ),
]

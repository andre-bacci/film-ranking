from django.urls import path

from .views import CompilationView, ListView

urlpatterns = [
    path(
        "<str:compilation_id>",
        ListView.as_view(actions={"get": "list", "post": "create"}),
    ),
    path(
        "<str:compilation_id>/<str:pk>", ListView.as_view(actions={"get": "retrieve"})
    ),
    path(
        "compilations/",
        CompilationView.as_view(actions={"get": "list", "post": "create"}),
    ),
    path("compilations/<str:pk>", CompilationView.as_view(actions={"get": "retrieve"})),
]

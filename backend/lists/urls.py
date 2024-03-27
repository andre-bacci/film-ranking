from django.urls import path

from .views import CompilationView

urlpatterns = [
    path(
        "compilations/",
        CompilationView.as_view(actions={"get": "list", "post": "create"}),
    ),
    path("compilations/<str:pk>", CompilationView.as_view(actions={"get": "retrieve"})),
]

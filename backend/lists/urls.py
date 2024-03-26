from django.urls import path

from .views import CompilationView

urlpatterns = [
    path("", CompilationView.as_view(actions={"get": "list"})),
    path("<str:pk>", CompilationView.as_view(actions={"get": "retrieve"})),
]

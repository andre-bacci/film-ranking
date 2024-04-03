from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import Login, UserView

urlpatterns = [
    path("login/", Login.as_view()),
    path("login/refresh/", TokenRefreshView.as_view(), name="login_refresh"),
    path("retrieve-self/", UserView.as_view(actions={"get": "retrieve_self"})),
]

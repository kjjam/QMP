from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from cash_managemnet.views import SignupView, LogOutView

urlpatterns = [
    path("signup", SignupView.as_view(), name="signup"),
    path("login", obtain_auth_token, name="login"),
    path("logout", LogOutView.as_view(), name="logout")
]

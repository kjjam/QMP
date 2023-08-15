from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from accounts.views import LogOutView, SignupView

urlpatterns = [
    path('login', obtain_auth_token, name="login"),
    path('logout', LogOutView.as_view(), name="logout"),
    path('signup', SignupView.as_view(), name="signup")
]
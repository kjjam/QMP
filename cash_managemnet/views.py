from rest_framework.authtoken.admin import User
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView

from cash_managemnet.serilalizers import SignupSerializer


class SignupView(CreateAPIView):
    model = User
    serializer_class = SignupSerializer


from rest_framework.authtoken.admin import User
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from cash_managemnet.serilalizers import SignupSerializer


class SignupView(CreateAPIView):
    model = User
    serializer_class = SignupSerializer


class LogOutView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        request.user.auth_token.delete()
        return Response({"username": request.user.username}, status=200)

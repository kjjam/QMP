from rest_framework.authtoken.admin import User
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.serilalizers import SignupSerializer


class SignupView(CreateAPIView):
    """
    info : Genetic View to create new User
        user creation manner is override in SignupSerializer
    headers =
        Content-Type : application/json
    method:
        POST
    response content-type :
        application/json
    response:
        {
            "username":<str:created-username>
        }
    """
    model = User  # model to create
    serializer_class = SignupSerializer  # serializer to validate input and create a user


class LogOutView(APIView):
    """
    info: logout user base on token-base authentication
        the user should be login to nbe logged out!
    headers =
        Content-Type : application/json
        Authorization : Token <token>
    method:
        GET
    response content-type :
        application/json
    response:
        {
            "username":<str:logged-out-username>
        }
    """
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        request.user.auth_token.delete()
        return Response({"username": request.user.username}, status=200)

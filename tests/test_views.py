from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.authtoken.admin import User

from rest_framework.authtoken.models import Token


def test_default_auth_model(self):
    self.assertEqual(get_user_model(), User, "Default auth-user-model is DRF user")


class TestSignUpView(TestCase):

    def test_sign_up_successful_return_201(self):
        username = "keyvan"
        password = "123456"
        response = self.client.post(reverse("signup"), data={"username": username, "password": password},
                                    content_type="application/json")
        self.assertEqual(response.status_code, 201, "Status code should be 201 !")
        self.assertEqual(response.data, {"username": "keyvan"}, "Response body should contain correct username only")

        registered_user = User.objects.get(username=username)
        self.assertTrue(registered_user.check_password(password), "Wrong password in database")

    def test_sign_up_duplicated_username_return_403(self):
        username = "keyvan"
        password = "123456"
        self.client.post(reverse("signup"), data={"username": username, "password": password},
                         content_type="application/json")
        duplicated_username = "keyvan"
        response = self.client.post(reverse("signup"), data={"username": duplicated_username, "password": password},
                                    content_type="application/json")
        self.assertEqual(response.status_code, 400, "Status code should be 400 !")


class TestLoginView(TestCase):
    def test_login_successful(self):
        username = "keyvan"
        password = "123456"
        user = User.objects.create_user(username=username, password=password)

        response = self.client.post(reverse("login"), data={"username": username, "password": password},
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200, "login status code should be 200")
        token = Token.objects.get(user=user)
        self.assertEqual(token.key, response.data["token"], "Wrong Token")

    def test_login_wrong_password_return_403(self):
        username = "keyvan"
        password = "123456"
        wrong_password = "123"
        user = User.objects.create_user(username=username, password=password)

        response = self.client.post(reverse("login"), data={"username": username, "password": wrong_password},
                                    content_type="application/json")
        self.assertEqual(response.status_code, 400, "login status code for bad password should be 400")


class TestLogout(TestCase):
    def test_logout_successful(self):
        username = "keyvan"
        password = "123456"
        User.objects.create_user(username=username, password=password)
        response = self.client.post(reverse("login"), data={"username": username, "password": password},
                                    content_type="application/json")

        token = response.data["token"]
        response = self.client.get(reverse("logout"),
                                   headers={
                                       "content_type": "application/json",
                                       "Authorization": "Token " + token
                                   })
        self.assertEqual(response.status_code, 200, "wrong status code for user logout on success")
        self.assertEqual(response.data, {"username": username}, "wrong content logout on success")

    def test_logout_not_login_return_401(self):
        response = self.client.get(reverse("logout"),
                                   headers={
                                       "content_type": "application/json",
                                   })
        self.assertEqual(response.status_code, 401, "wrong status code for user logout on empty token")

    def test_logout_bad_login_return_401(self):
        response = self.client.get(reverse("logout"),
                                   headers={
                                       "content_type": "application/json",
                                       "Authorization": "Token " + "blabla"

                                   })
        self.assertEqual(response.status_code, 401, "wrong status code for user logout on empty token")

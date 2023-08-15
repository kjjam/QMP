from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.authtoken.admin import User


class TestSignUpView(TestCase):

    def test_default_auth_model(self):
        self.assertEqual(get_user_model(), User, "Default auth-user-model is DRF user")

    def test_sign_up_successful_return_201(self):
        username = "keyvan"
        password = "123456"
        response = self.client.post(reverse("signup"), data={"username": username, "password": password},
                                    content_type="application/json")
        self.assertEqual(response.status_code, 201, "Status code should be 201 !")
        self.assertEqual(response.data, {"username": "keyvan"}, "Response body should contain correct username only")

    def test_sign_up_duplicated_username_return_403(self):
        username = "keyvan"
        password = "123456"
        self.client.post(reverse("signup"), data={"username": username, "password": password}, content_type="application/json")
        duplicated_username = "keyvan"
        response = self.client.post(reverse("signup"), data={"username": duplicated_username, "password": password},
                                    content_type="application/json")
        self.assertEqual(response.status_code, 400, "Status code should be 400 !")

import datetime
import json

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.authtoken.admin import User
from rest_framework.authtoken.models import Token

from cash_managemnet.models import Transaction


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


class TestLogoutView(TestCase):
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


class TestCreateTransactionView(TestCase):
    username = "keyvan"
    password = "123456"

    def setUp(self):
        self.token = self._login()

    def _logout(self):
        Token.objects.get(user__username=self.username).delete()

    def _login(self):
        user = User.objects.create_user(username=self.username, password=self.password)
        response = self.client.post(reverse("login"), data={"username": self.username, "password": self.password},
                                    content_type="application/json")
        return response.data['token']

    def _request(self, url, data, method="POST"):
        content_type = "application/json"
        headers = {"Authorization": f"Token {self.token}"}

        if method == "POST":
            return self.client.post(url, data, content_type=content_type, headers=headers)
        elif method == "PUT":
            return self.client.put(url, data, content_type=content_type, headers=headers)
        elif method == "PATCH":
            return self.client.patch(url, data, content_type=content_type, headers=headers)
        else:
            return self.client.get(url, data, content_type=content_type, headers=headers)

    def test_insert_transaction_user_not_login(self):
        self._logout()
        response = self._request(reverse("insert-transaction"), {"amount": 200, "type": "I"}, "POST")
        self.assertEqual(response.status_code, 401, "should return response with 401 status code")

    # test existent and not-existent of the amount field
    def test_insert_transaction_amount_required(self):
        # checks if 'amount' is not in request, bad request returns
        data_without_amount = {"type": "I"}
        response1 = self._request(reverse("insert-transaction"), data_without_amount, "POST")
        self.assertEqual(response1.status_code, 400, "Amount is needed")

        # checks if 'amount' is in request, 201 returns
        response2 = self.client.post(reverse("insert-transaction"),
                                     data=json.dumps({"amount": 200, "type": "I"}),
                                     content_type="application/json",
                                     headers={
                                         "Authorization": f"Token {self.token}"}
                                     )
        new_transaction = Transaction.objects.get(id=response2.data["id"])
        self.assertEqual(new_transaction.amount, 200)
        self.assertEqual(response2.status_code, 201, "Amount is provided so it is ok!")

    # The current authenticated user should be the creator of the transaction.
    def test_insert_transaction_user_owner(self):
        data = {"amount": 200, "type": "I"}
        response = self._request(reverse("insert-transaction"), data, "POST")
        transaction_id = response.data["id"]
        self.assertEqual(Transaction.objects.get(id=transaction_id).user.username, self.username,
                         "the owner should be the creator")

    # The 'type' should be 'I' of 'E' not the other values
    def test_insert_transaction_wrong_type_value(self):
        bad_types = ["EE", "E E", "II", "I I", "BadEI"]
        for b in bad_types:
            data = {"amount": 200, "type": b}
            response = self._request(reverse("insert-transaction"), data, "POST")
            self.assertEqual(response.status_code, 400, "Bad type value should return bad request")

    # The 'type' should be 'I' of 'E'.
    def test_insert_transaction_correct_type_value(self):
        for t in Transaction.TypeChoices.choices:
            good_type = {"amount": 200, "type": t[0]}
            response = self._request(reverse("insert-transaction"), good_type, "POST")
            new_transaction = Transaction.objects.get(id=response.data["id"])
            self.assertEqual(new_transaction.type, t[0])
            self.assertEqual(response.status_code, 201, "Type value is good.  should be saved")

    def test_insert_transaction_type_required(self):
        # checks if 'type' is not in request, bad request returns
        response1 = self._request(reverse("insert-transaction"), {"amount": 100}, "POST")
        self.assertEqual(response1.status_code, 400, "type is needed")

        # checks if 'type' is in request, 201 returns
        response2 = self._request(reverse("insert-transaction"), {"type": "I", "amount": 100}, "POST")
        new_transaction = Transaction.objects.get(id=response2.data["id"])
        self.assertEqual(new_transaction.type, "I")
        self.assertEqual(response2.status_code, 201, "type is provided so it is ok!")

    def test_insert_transaction_date_not_input_auto_create(self):
        data = {"amount": 10, "type": "I"}
        response1 = self._request(reverse("insert-transaction"), data, "POST")
        new_transaction = Transaction.objects.get(id=response1.data["id"])
        self.assertTrue("2023" in str(new_transaction.date), "date should be filled automatically")

    def test_insert_transaction_date_input(self):
        data = {"amount": 10, "type": "I", "date": "2020-02-02T18:30:00-04:00"}
        response1 = self._request(reverse("insert-transaction"), data, "POST")
        new_transaction = Transaction.objects.get(id=response1.data["id"])
        self.assertEqual(datetime.datetime.fromisoformat(data["date"]), new_transaction.date,
                         "date should be filled automatically")


class TestDeleteTransactionView(TestCase):
    username = "keyvan"
    password = "123456"

    def setUp(self):
        self.token = self._login(self.username, self.password)

    def _logout(self, username):
        Token.objects.get(user__username=username).delete()

    def _login(self, username, password):
        user = User.objects.create_user(username=username, password=password)
        response = self.client.post(reverse("login"), data={"username": username, "password": password},
                                    content_type="application/json")
        return response.data['token']

    def _request(self, url, data, token, method="POST"):
        content_type = "application/json"
        headers = {"Authorization": f"Token {token}"}

        if method == "POST":
            return self.client.post(url, data, content_type=content_type, headers=headers)
        elif method == "PUT":
            return self.client.put(url, data, content_type=content_type, headers=headers)
        elif method == "PATCH":
            return self.client.patch(url, data, content_type=content_type, headers=headers)
        elif method == "DELETE":
            return self.client.delete(url, data, content_type=content_type, headers=headers)
        else:
            return self.client.get(url, data, content_type=content_type, headers=headers)

    def test_delete_transaction_not_login(self):
        self._logout(self.username)
        response = self._request(reverse("delete-transaction", args=[1]), {}, self.token, "POST")
        self.assertEqual(response.status_code, 401, "should return response with 401 status code")

    def test_delete_transaction_not_found(self):
        response = self._request(reverse("delete-transaction", args=[1]), {}, "DELETE")
        self.assertEqual(response.status_code, 404, "Transaction should not be found")

    def test_delete_transaction_delete_another_user_transaction(self):
        another_token = self._login("another user", "123456")
        response1 = self._request(reverse("insert-transaction"), {"amount": 10, "type": "E"}, another_token,
                                  "POST")
        new_transaction = Transaction.objects.get(id=response1.data["id"])
        self._logout("another user")

        self.assertEqual(Transaction.objects.filter(user__username='another user').count(), 1)
        self.assertEqual(Transaction.objects.all().count(), 1)

        reponse2 = self._request(reverse("delete-transaction", args=[new_transaction.id]), {}, self.token, "DELETE")
        self.assertEqual(reponse2.status_code, 404, "This transaction is not found for current user")
        self.assertEqual(Transaction.objects.filter(user__username='another user').count(), 1)
        self.assertEqual(Transaction.objects.all().count(), 1)



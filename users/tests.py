from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase


class UsersTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username="username")
        self.user.set_password("password")
        self.user.save()
        self.access_url = '/user/token'
        self.refresh_url = '/user/token/refresh'


    def test_retrieve_access_token(self):
        refresh = self.client.post(
            self.access_url,
            data={
                "username": "username",
                "password": "password",
            },
            format="json"
        )
        self.assertEqual(refresh.status_code, status.HTTP_200_OK)

    def test_refresh_token(self):
        token = self.client.post(
            self.access_url,
            data={
                "username": "username",
                "password": "password",
            },
            format="json"
        )
        self.assertEqual(token.status_code, status.HTTP_200_OK)
        token = token.json()
        assert "access" in token, "Access token not returned"
        assert "refresh" in token, "Refresh token not returned"

        refresh_token = token["refresh"]

        response = self.client.post(
            self.refresh_url,
            data={"refresh": refresh_token},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert "access" in response.json(), "Access token not returned"

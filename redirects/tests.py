from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from url_managements.models import RedirectRule

class RedirectRulesTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username="username")
        self.user.set_password("password")
        self.user.save()

        self.token = self.get_token(self.user)
        self.headers = {"Authorization": f"Bearer {self.token}"}
        self.url = "/redirect"
        self.redirect_rule_private = RedirectRule.objects.create(
            redirect_url="https://example.com",
            is_private=True,
            owner=self.user,
        )
        self.redirect_rule_public = RedirectRule.objects.create(
            redirect_url="https://example.com",
            is_private=False,
            owner=self.user,
        )

    def get_token(self, user):
        token = self.client.post(
            "/user/token",
            data={
                "username": "username",
                "password": "password",
            },
            format="json"
        )
        return token.json()["access"]

    def test_get_private(self):
        response = self.client.get(
            f"{self.url}/private/{self.redirect_rule_private.redirect_identifier}",
            headers=self.headers,
        )
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertIsInstance(response_json, dict)

        self.assertEqual(response_json.get("redirect_url"), self.redirect_rule_private.redirect_url)
        self.assertEqual(response_json.get("redirect_identifier"), self.redirect_rule_private.redirect_identifier)

        response = self.client.get(
            f"{self.url}/public/{self.redirect_rule_private.redirect_identifier}"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_public(self):
        response = self.client.get(
            f"{self.url}/public/{self.redirect_rule_public.redirect_identifier}"
        )
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertIsInstance(response_json, dict)

        self.assertEqual(response_json.get("redirect_url"), self.redirect_rule_public.redirect_url)
        self.assertEqual(response_json.get("redirect_identifier"), self.redirect_rule_public.redirect_identifier)

        response = self.client.get(
            f"{self.url}/public/{self.redirect_rule_private.redirect_identifier}",
            headers=self.headers,
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

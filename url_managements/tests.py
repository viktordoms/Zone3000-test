from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from url_managements.models import RedirectRule


class RedirectRulesManagersTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username="username")
        self.user.set_password("password")
        self.user.save()

        self.token = self.get_token(self.user)
        self.headers = {"Authorization": f"Bearer {self.token}"}
        self.url = "/url"
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

    def test_get_list(self):
        response = self.client.get(self.url, headers=self.headers)
        response_json = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response_json, list)
        self.assertIsInstance(response_json[0], dict)

    def test_create_instance(self):
        data = {"redirect_url": "https://example.com", "is_private": False}
        response = self.client.post(
            self.url,
            data=data,
            headers=self.headers
        )
        response_json = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsInstance(response_json, dict)
        self.assertEqual(
            response_json, {"owner": self.user.pk, **data}
        )

    def test_update_instance(self):
        url = f"{self.url}/{self.redirect_rule_public.id}"
        response = self.client.patch(
            url, {"is_private": True}, headers=self.headers
        )
        response_json = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response_json, dict)
        self.assertEqual(response_json["is_private"], True)
        self.assertEqual(response_json["owner"], self.user.pk)

        updated_instance = RedirectRule.objects.get(pk=self.redirect_rule_public.id)
        self.assertEqual(updated_instance.is_private, True)


    def test_delete_instance(self):
        url = f"{self.url}/{self.redirect_rule_public.id}"
        response = self.client.delete(url, headers=self.headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        instance = RedirectRule.objects.filter(pk=self.redirect_rule_public.id).count()
        self.assertEqual(instance, 0)

        response =  self.client.delete(url, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
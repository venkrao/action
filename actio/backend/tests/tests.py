from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from django.urls import reverse
from rest_framework import status

from actio.settings import SIMPLE_JWT

User = get_user_model()


class JwtTokenRetrieval(APITestCase):
    def setUp(self):
        data = {"username": "testuser_1", "password": "Dummypwd1"}
        user = User.objects.create_user(username=data.get("username"), password=data.get("password"))
        url = reverse("token_obtain_pair")
        self.jwt_response = self.client.post(url, data)
        self.assertEqual(self.jwt_response.status_code, status.HTTP_200_OK)

    def test_jwt_token_generation_should_return_http_200(self):
        self.assertEqual(self.jwt_response.status_code, status.HTTP_200_OK)

    def test_jwt_token_generation_should_return_access_and_refresh_token(self):
        self.assertNotEqual(self.jwt_response.data.get("access", ""), "")
        self.assertNotEqual(self.jwt_response.data.get("refresh", ""), "")

    def tearDown(self):
        pass


class TestTwilioRoomHandlerView(APITestCase):
    view_name = 'twilio-room-handler'
    url = reverse(view_name)

    def setUp(self):
        data = {"username": "testuser_1", "password": "Dummypwd1"}
        self.user = User.objects.create_user(username=data.get("username"), password=data.get("password"))
        url = reverse("token_obtain_pair")
        self.jwt_response = self.client.post(url, data)
        self.token = self.jwt_response.data.get("access")

    def test_request_without_jwt_should_return_unauthorized_response(self):
        res = self.client.post(self.url, {})
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_(self):
        res = self.client.post(self.url, {})
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


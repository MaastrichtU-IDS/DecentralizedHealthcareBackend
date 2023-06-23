from django.urls import reverse
from rest_framework.test import APIRequestFactory, APITestCase, APIClient

from .data_template import get_registration_data


class UserLoginTest(APITestCase):
    def setUp(self):
        self.registration_data = get_registration_data()

        self.login_data = {
            "username": self.registration_data['email'],
            "password": self.registration_data['password'],
        }
        self.client = APIClient()

        self.client.post(reverse('user-register'), self.registration_data)

    def test_login(self):
        # login
        response = self.client.post(reverse('user-login'), self.login_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['error']['code'], 200)
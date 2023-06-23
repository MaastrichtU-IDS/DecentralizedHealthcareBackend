from django.urls import reverse
from rest_framework.test import APIRequestFactory, APITestCase, APIClient

from .data_template import get_registration_data


class LUCERegistryTest(APITestCase):
    def setUp(self):
        self.registration_data = get_registration_data()

        self.login_data = {
            "username": self.registration_data['email'],
            "password": self.registration_data['password'],
        }
        self.client = APIClient()

        self.client.post(reverse('user-register'), self.registration_data)

        # login
        response = self.client.post(reverse('user-login'), self.login_data)
        self.token = response.data['data']['token']

    def test_deploy_LUCERegistry(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(reverse('admin-deployRegistry'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['error']['code'], 200)
        # self.assertEqual(response.data['data
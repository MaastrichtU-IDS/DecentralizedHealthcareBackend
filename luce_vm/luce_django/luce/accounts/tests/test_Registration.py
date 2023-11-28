from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from accounts.models import User
from brownie import network


class RegistrationTestCase(TestCase):
    def setUp(self):
        self.data = {
            'username': 'testuser',
            'email': 'test@email.com',
            'password': 'testpassword',
        }
        self.client = APIClient()
        self.registration_url = reverse('user_registration')

    def test_valid_registration(self):
        response = self.client.post(self.registration_url, self.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 1)

        is_connected = network.is_connected()
        print("is_connected: ", is_connected)
        if is_connected:
            network.disconnect()

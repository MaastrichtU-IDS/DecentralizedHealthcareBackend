from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from accounts.models import User


class LoginTestCase(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(
            email='test@example.com',
            password='testpassword',
            gender='m',
            age=20,
            first_name='test',
            last_name='user',
        )
        self.client = APIClient()
        self.login_url = reverse('login')

    def test_login_success(self):
        data = {
            'username': 'test@example.com',
            'password': 'testpassword'
        }

        response = self.client.post(self.login_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data['data'])

from django.test import TestCase

from django.urls import reverse
from accounts.models import User


class RegistrationTestCase(TestCase):
    def test_valid_registration(self):
        data = {
            'username': 'testuser',
            'email': 'test@email.com',
            'password': 'testpassword',
        }
        response = self.client.post(reverse('user_registration'), data)
        # print("here")
        # print(response.data)
        self.assertEqual(response.status_code, 200)  # expecting a redirect
        self.assertEqual(User.objects.count(), 1)  # a user should be created
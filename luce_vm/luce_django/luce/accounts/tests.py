from django.test import TestCase

from django.urls import reverse
# from django.contrib.auth.models import User
from accounts.models import User


class RegistrationTestCase(TestCase):
    def test_valid_registration(self):
        data = {
            'username': 'testuser',
            'email': 'test@email.com',
            'password': 'testpassword',
        }
        response = self.client.post(reverse('register'), data)
        # print("here")
        # print(response)
        self.assertEqual(response.status_code, 200)  # expecting a redirect
        self.assertEqual(User.objects.count(), 1)  # a user should be created

    # def test_invalid_registration(self):
    #     data = {
    #         'username': '',
    #         'email': 'test@email.com',
    #         'password': 'testpassword',
    #     }
    #     response = self.client.post(reverse('register'), data)
    #     self.assertEqual(response.status_code, 200)  # staying on the same page
    #     self.assertEqual(User.objects.count(), 0)  # no user should be created

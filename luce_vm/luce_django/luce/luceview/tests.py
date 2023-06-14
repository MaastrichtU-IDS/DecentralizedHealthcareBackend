from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIRequestFactory, APITestCase, APIClient

from accounts.models import User
from luceview.views import UserRegistration

# Create your tests here.

# class UploadDataViewTests(TestCase):
#     def setUp(self):
#         self.username = 'likun6034@gmail.com'
#         self.password = '1'
#         self.user = User.objects.create_user(
#             username=self.username,
#             password=self.password
#         )

#         self.client = Client()
#         self.client.login(username=self.username, password=self.password)


class UserRegistrationTests(APITestCase):
    def test_registration(self):
        data = {
            "last_name": "piccini",
            "email": "email2@email.com",
            "password": "password123",
            "create_wallet": True,
            "user_type": 0
        }

        url = reverse('user-register')
        client = APIClient()
        response = client.post(url, data, format='json')
        # print(response)
        self.assertEqual(response.status_code, 200)

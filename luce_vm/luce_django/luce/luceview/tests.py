from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIRequestFactory, APITestCase, APIClient

from accounts.models import User

from luceview.serializers import UserSerializer
from luceview.views import UserRegistration

# Create your tests here.

# class UserRegistrationTest(APITestCase):
#     def setUp(self):
#         self.registration_data = {
#             "last_name": "piccini",
#             "email": "email@email.com",
#             "password": "password123",
#             "create_wallet": True,
#             "user_type": 0
#         }

#         self.client = APIClient()
#         self.url = reverse('user-register')

#     def test_registration(self):
#         response = self.client.post(self.url,
#                                     self.registration_data,
#                                     format='json')

#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.data['error']['code'], 200)

# class UserLoginTest(APITestCase):
#     def setUp(self):
#         self.registration_data = {
#             "last_name": "piccini",
#             "email": "email1@email.com",
#             "password": "password123",
#             "create_wallet": True,
#             "user_type": 0
#         }

#         self.login_data = {
#             "username": self.registration_data['email'],
#             "password": self.registration_data['password'],
#         }

#         self.client = APIClient()
#         # self.url = reverse('user-login')

#     def test_login(self):
#         # registration
#         response = self.client.post(reverse('user-register'),
#                                     self.registration_data,
#                                     format='json')
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.data['error']['code'], 200)

#         # login
#         response = self.client.post(reverse('user-login'), self.login_data)
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.data['error']['code'], 200)


class UploadDataTest(APITestCase):
    def setUp(self):
        self.registration_data = {
            "last_name": "piccini",
            "email": "email2@email.com",
            "password": "password123",
            "create_wallet": True,
            "user_type": 0
        }

        self.login_data = {
            "username": self.registration_data['email'],
            "password": self.registration_data['password'],
        }

        print(self.login_data)

        self.uploaded_data = {
            "estimate": False,
            "description": "ds",
            "link": "http://link.com",
            "no_restrictions": False,
            "open_to_general_research_and_clinical_care": False,
            "open_to_HMB_research": False,
            "open_to_population_and_ancestry_research": False,
            "open_to_disease_specific": False
        }

        self.client = APIClient()

    def test_upload_data(self):
        response = self.client.post(reverse('user-register'),
                                    self.registration_data,
                                    format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['error']['code'], 200)

        # login
        response = self.client.post(reverse('user-login'), self.login_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['error']['code'], 200)

        login_token = response.data['data']['token']
        # upload data

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + login_token)

        response = self.client.post(reverse('contract-dataUpload'),
                                    self.uploaded_data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['error']['code'], 200)

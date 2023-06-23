from django.urls import reverse
from rest_framework.test import APIRequestFactory, APITestCase, APIClient

# from luceview.views import UserRegistration
from .data_template import get_registration_data


class UserRegistrationTest(APITestCase):
    def setUp(self):
        self.registration_data = get_registration_data()
        self.client = APIClient()

    def test_registration_success(self):
        response = self.client.post(reverse('user-register'),
                                    self.registration_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['error']['code'], 200)

from django.urls import reverse
from rest_framework.test import APIRequestFactory, APITestCase, APIClient

from .data_template import get_registration_data


class UploadDataTest(APITestCase):
    def setUp(self):
        self.registration_data = get_registration_data()

        self.login_data = {
            "username": self.registration_data['email'],
            "password": self.registration_data['password'],
        }

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

        # register
        response = self.client.post(reverse('user-register'),
                                    self.registration_data,
                                    format='json')

        # login
        response = self.client.post(reverse('user-login'), self.login_data)

        login_token = response.data['data']['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + login_token)

        # deploy LUCERegistry
        response = self.client.post(reverse('admin-deployRegistry'))

        # upload data
        response = self.client.post(reverse('contract-dataUpload'),
                                    self.uploaded_data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['error']['code'], 200)

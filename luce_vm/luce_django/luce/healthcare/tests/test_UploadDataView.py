from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from accounts.models import User

from blockchain.models import LuceRegistryContract


class UploadDataViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.upload_data_url = reverse('upload_data_view')
        self.registration_url = reverse('user_registration')
        self.login_url = reverse('login')
        self.deploy_registry_url = reverse('deploy_registry_view')

        self.data_registration = {
            "last_name": "piccini",
            "email": "email2@email.com",
            "password": "password123",
            "create_wallet": True,
            "user_type": 0
        }

        self.data_login = {
            "username": self.data_registration['email'],
            "password": self.data_registration['password']
        }

        self.data = {
            "estimate": False,
            "description": "ds",
            "link": "http://link.com",
            "no_restrictions": False,
            "open_to_general_research_and_clinical_care": False,
            "open_to_HMB_research": False,
            "open_to_population_and_ancestry_research": False,
            "open_to_disease_specific": False
        }

    def deploy_registry(self):
        deployed = self.client.post(self.deploy_registry_url, format='json')

        return deployed

    def register_user(self, data_registration):
        response = self.client.post(self.registration_url,
                                    data_registration,
                                    format='json')
        return response

    def login_user(self, data_login):
        response = self.client.post(self.login_url, data_login, format='json')
        return response

    def test_upload_data_view(self):

        registration_response = self.register_user(self.data_registration)
        print("registration_response", registration_response.data)

        user = User.objects.get(email=self.data_registration['email'])
        self.client.force_authenticate(user=user)

        deployed_registry = self.deploy_registry()
        print("deployed_registry", deployed_registry)

        response = self.client.post(self.upload_data_url,
                                    self.data,
                                    format='json')
        print("response", response.data)
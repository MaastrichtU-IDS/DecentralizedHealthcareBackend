from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from accounts.models import User
from blockchain.models import LuceRegistryContract


class RequestDatasetViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.request_dataset_url = reverse('request_dataset_view')
        self.registration_url = reverse('user_registration')
        self.login_url = reverse('login')
        self.deploy_registry_url = reverse('deploy_registry_view')
        self.upload_data_url = reverse('upload_data_view')

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

        self.data_upload = {
            "estimate": False,
            "description": "ds",
            "link": "http://link.com",
            "no_restrictions": False,
            "open_to_general_research_and_clinical_care": False,
            "open_to_HMB_research": False,
            "open_to_population_and_ancestry_research": False,
            "open_to_disease_specific": False
        }

        self.data_access = {
            "estimate": False,
            "dataset_addresses": ["0x0"],
            "general_research_purpose": {
                "use_for_methods_development": True,
                "use_for_reference_or_control_material": True,
                "use_for_populations_research": True,
                "use_for_ancestry_research": True,
                "use_for_HMB_research": True
            },
            "HMB_research_purpose": {
                "use_for_research_concerning_fundamental_biology": False,
                "use_for_research_concerning_genetics": False,
                "use_for_research_concerning_drug_development": False,
                "use_for_research_concerning_any_disease": False,
                "use_for_research_concerning_age_categories": False,
                "use_for_research_concerning_gender_categories": False
            },
            "clinical_purpose": {
                "use_for_decision_support": False,
                "use_for_disease_support": False
            }
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

    def upload_data(self, data_upload):
        registration_response = self.register_user(self.data_registration)
        print("registration_response", registration_response.data)

        user = User.objects.get(email=self.data_registration['email'])
        self.client.force_authenticate(user=user)

        deployed_registry = self.deploy_registry()
        print("deployed_registry", deployed_registry)

        response = self.client.post(self.upload_data_url,
                                    self.data_upload,
                                    format='json')
        print("Upload response:\n",
              response.data["data"]["contracts"]["contract_address"])
        return response.data["data"]["contracts"]["contract_address"]

    def test_access_data_view(self):
        upload_data_address = self.upload_data(self.data_upload)

        self.data_access["dataset_addresses"] = [upload_data_address]
        access_response = self.client.post(self.request_dataset_url,
                                           self.data_access,
                                           format='json')

        print("access_response", access_response.data)

from django.test import TestCase
from blockchain.models import LuceRegistryContractSingleton


class LuceRegistryContractSingletonModelTestCase(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            'admin', 'admin@example.com', 'password')

    def test_deploy(self):
        luce_registry_contract_singleton = LuceRegistryContractSingleton.load()

        print("luce_registry_contract_singleton: ",
              luce_registry_contract_singleton)

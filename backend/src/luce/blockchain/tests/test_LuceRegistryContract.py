from django.test import TestCase
from accounts.models import User
from blockchain.models import LuceRegistryContract


class LuceRegistryContractModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='exmaple@test.com',
                                             password='testpassword',
                                             first_name='test',
                                             last_name='user',
                                             age=20,
                                             gender='M')
        self.luce_registry_contract = LuceRegistryContract.objects.create(
            user=self.user, contract_address='0xSomeAddress')

    def test_deploy(self):
        self.assertEqual(self.luce_registry_contract.deploy(), 1)

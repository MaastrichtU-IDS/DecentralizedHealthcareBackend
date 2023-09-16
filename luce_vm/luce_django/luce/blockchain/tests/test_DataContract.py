from django.test import TestCase
from accounts.models import User
from blockchain.models import DataContract


class DataContractModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='exmaple@test.com',
                                             password='testpassword',
                                             first_name='test',
                                             last_name='user',
                                             age=20,
                                             gender='M')
        self.data_contract = DataContract.objects.create(
            user=self.user, contract_address='0xSomeAddress')

    def test_deploy(self):
        deployed = self.data_contract.deploy()
        # print(deployed)
        self.assertEqual(deployed.status, 1)
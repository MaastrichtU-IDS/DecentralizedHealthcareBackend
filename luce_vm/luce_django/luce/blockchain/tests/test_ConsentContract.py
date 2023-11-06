from django.test import TestCase
from accounts.models import User
from blockchain.models import ConsentContract
from blockchain.models import Restrictions
from blockchain.models import ResearchPurpose


class ConsentContractModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='exmaple@test.com',
                                             password='testpassword',
                                             first_name='test',
                                             last_name='user',
                                             age=20,
                                             gender='M')
        self.restrictions = Restrictions.objects.create()
        self.research_purpose = ResearchPurpose.objects.create()

        self.consent_contract = ConsentContract.objects.create(
            contract_address='0xSomeAddress')

    def test_deploy(self):
        deployed = self.consent_contract.deploy()
        self.assertEqual(deployed.status, 1)
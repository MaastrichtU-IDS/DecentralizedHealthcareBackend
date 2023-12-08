from django.test import TestCase
from blockchain.models import PrivacyShieldDatasetContract, PlonkVerifierContract
from . import helper


class PrivacyShieldDatasetContractModelTestCase(TestCase):
    def setUp(self):
        self.user = helper.create_user()
        self.research_purpose = helper.create_research_purpose()
        self.restrictions = helper.create_restrictions()
        self.consent_contract = helper.create_consent_contract(
            self.user,
            self.research_purpose,
            self.restrictions
        )

        self.privacy_shield_dataset_contract = PrivacyShieldDatasetContract.objects.create(
            user=self.user,
            contract_address='0x0',
            commitment='0x0',
            consent_contract=self.consent_contract,
            description='test description',
            licence=1,
            link='test link'
        )

    def test_deploy(self):
        privacy_shield_dataset_contract_deploy = self.privacy_shield_dataset_contract.deploy()
        print(privacy_shield_dataset_contract_deploy)
        self.assertEqual(privacy_shield_dataset_contract_deploy, 1)

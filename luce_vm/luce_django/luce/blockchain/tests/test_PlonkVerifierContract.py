from django.test import TestCase
from blockchain.models import PlonkVerifierContract


class PlonkVerifierContractModelTestCase(TestCase):
    def setUp(self):
        # self.user = User.objects.create_user(
        self.plonk_verifier_contract = PlonkVerifierContract.objects.create(
            name='test', address='0xSomeAddress')

    def test_deploy(self):
        plonk_verifier_contract_deploy = self.plonk_verifier_contract.deploy()
        print(plonk_verifier_contract_deploy)
        self.assertEqual(plonk_verifier_contract_deploy.status, 1)

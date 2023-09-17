from django.test import TestCase
from privacy.models import MimicMixingServiceContract


class MimicMixingServiceContractModelTestCase(TestCase):
    def setUp(self):
        self.mimic_mixing_service_contract = MimicMixingServiceContract.objects.create(
        )

    def test_deploy(self):
        deployed = self.mimic_mixing_service_contract.deploy()
        self.assertEqual(deployed.status, 1)

    def test_deposit(self):
        deposited = self.mimic_mixing_service_contract.deposit()
        # print(deposited)
        self.assertEqual(deposited.status, 1)
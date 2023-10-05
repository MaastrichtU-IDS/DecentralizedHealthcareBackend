from django.test import TestCase
from privacy.models import MimicMixingServiceContract
from brownie import accounts


class MimicMixingServiceContractModelTestCase(TestCase):
    def setUp(self):
        """
        Set up the MimicMixingServiceContract model test case.
        In this step, we create a MimicMixingServiceContract instance, which deploys the contract.
        """
        self.mimic_mixing_service_contract = MimicMixingServiceContract.load()

    # def test_deploy(self):
    #     deployed = self.mimic_mixing_service_contract.deploy()
    #     self.assertEqual(deployed.status, 1)

    def test_str(self):
        """
        Test the string representation of the MimicMixingServiceContract model.
        """
        # print(self.mimic_mixing_service_contract)
        print("test_str")
        self.assertEqual(str(self.mimic_mixing_service_contract),
                         self.mimic_mixing_service_contract.contract_address)

    def test_is_deployed(self):
        """
        Test the is_deployed method of the MimicMixingServiceContract model.
        """
        print("test_is_deployed")
        self.assertTrue(self.mimic_mixing_service_contract.is_deployed())

    def test_deposit(self):
        balance_before_deposit = self.mimic_mixing_service_contract.balance()
        print(f"balance_before_deposit: {balance_before_deposit}")
        sender = accounts[0]
        amount = 1000000000000000000
        deposited = self.mimic_mixing_service_contract.deposit(sender=sender,
                                                               amount=amount)
        balance_after_deposit = self.mimic_mixing_service_contract.balance()
        print(f"balance_after_deposit: {balance_after_deposit}")

        self.assertEqual(deposited.status, 1)
        self.assertEqual(balance_after_deposit,
                         balance_before_deposit + amount)

    # def test_withdraw(self):
    #     from brownie import accounts
    #     withdrawn = self.mimic_mixing_service_contract.withdraw(
    #         accounts.add(), 1000000000000000000)
    #     self.assertEqual(withdrawn.status, 1)

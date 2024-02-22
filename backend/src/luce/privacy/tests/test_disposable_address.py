from django.test import TestCase
from privacy.disposable_address import DisposableAddressService
from brownie import accounts


class DisposableAddressServiceTests(TestCase):
    def setUp(self):
        self.disposable_address_service = DisposableAddressService()
        self.sender = accounts[0]
        self.amount = 1000000000000000000

    def test_get_a_new_address(self):
        new_address = self.disposable_address_service.get_a_new_address()
        self.assertIsNotNone(new_address)

    def test_get_a_new_address_with_balance(self):
        self.disposable_address_service.get_a_new_address_with_balance(
            self.sender, self.amount)
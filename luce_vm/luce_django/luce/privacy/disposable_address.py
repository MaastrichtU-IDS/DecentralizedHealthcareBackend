from brownie import accounts
from .models import MimicMixingServiceContract


class DisposableAddressService:
    """
    This service provides functionalities to get disposable addresses. Implemented as a Singleton.
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            print("Creating a new DisposableAddressService instance.")
            cls._instance = super(DisposableAddressService, cls).__new__(cls)
        return cls._instance

    def get_a_new_address(self) -> str:
        """
        Generates a new address and returns it.

        Returns:
            str: Newly generated address.
        """
        return accounts.add()

    def get_a_new_address_with_balance(self, sender: str, amount: int) -> str:
        """
        Generates a new address, transfers a given amount to it, 
        and returns the address.

        Parameters:
            sender (str): Address of the sender.
            amount (int): Amount to transfer.

        Returns:
            str: Newly generated address with balance.
        """
        # TODO: Validate sender and amount

        new_address = accounts.add()

        mixing_service = MimicMixingServiceContract.load()

        if not mixing_service.is_deployed():
            mixing_service.deploy()

        balance_before_deposit = mixing_service.balance()
        print(f"balance_before_deposit: {balance_before_deposit}")

        deposited = mixing_service.deposit(sender, amount)

        balance_after_deposit = mixing_service.balance()
        print(f"balance_after_deposit: {balance_after_deposit}")

        withdrawn = mixing_service.withdraw(new_address, amount)
        # print(f"withdrawn: {withdrawn}")

        new_address_balance = new_address.balance()
        print(f"new_address_balance: {new_address_balance}")

        return new_address


# # Test the Singleton implementation
# service1 = DisposableAddressService()
# service2 = DisposableAddressService()

# # Should print "Creating a new DisposableAddressService instance." only once
# # Both service1 and service2 will point to the same object
# print(service1 is service2)  # Should print True

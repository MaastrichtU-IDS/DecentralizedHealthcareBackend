import logging

from brownie import accounts
from .models import MimicMixingServiceContract

# Configure logging at the start of your script
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s: [%(levelname)s] %(message)s'
)


class DisposableAddressService:
    """
    This service provides functionalities to get disposable addresses. Implemented as a Singleton.
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            logging.info("Creating a new DisposableAddressService instance.")
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
        logging.info("mixing_service: %s", mixing_service)
        logging.info(
            "mixing_service.is_deployed(): %s",
            mixing_service.is_deployed()
        )

        logging.info(
            "mixing_service.contract_address: %s",
            mixing_service.contract_address
        )

        if not mixing_service.is_deployed():
            mixing_service.deploy()

        balance_before_deposit = mixing_service.balance()
        logging.info("balance_before_deposit: %s", balance_before_deposit)

        deposited = mixing_service.deposit(sender, amount)

        balance_after_deposit = mixing_service.balance()
        logging.info("balance_after_deposit: %s", balance_after_deposit)

        withdrawn = mixing_service.withdraw(new_address, amount)
        # logging.info(f"withdrawn: {withdrawn}")

        new_address_balance = new_address.balance()
        logging.info("balance of %s : %s", new_address, new_address_balance)

        return new_address

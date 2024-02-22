# from django.db import models
from brownie import accounts
from blockchain.models import SingletonContractModel


class MimicMixingServiceContract(SingletonContractModel):
    """
    Model to store the MimicMixingService contract address.
    """
    default_contract_name = "MimicMixingService"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.contract_name = self.default_contract_name

    def __str__(self):
        return self.contract_name

    # def save(self, *args, **kwargs):
    #     # self.contract_name = self.default_contract_name
    #     self.contract_address = self.deployed_address
    #     super().save(*args, **kwargs)

    def balance(self):
        """
        Function to get the balance of the MimicMixingService contract.
        """
        from brownie.project.BrownieProject import MimicMixingService

        self.require_deployed()
        balance = MimicMixingService.at(self.contract_address).balance()

        return balance

    def deploy(self):
        """
        Function to deploy the MimicMixingService contract.
        """
        # from brownie import accounts, MimicMixingService
        from brownie.project.BrownieProject import MimicMixingService

        deployed = MimicMixingService.deploy({'from': accounts[0]})
        self.contract_address = deployed.address
        self.save()

        return deployed.tx

    def is_deployed(self):
        """
        Function to check if the MimicMixingService contract is deployed.
        """
        if self.contract_address is not None:
            return True
        else:
            return False

    def require_deployed(self):
        """
        Function to check if the MimicMixingService contract is deployed.
        """
        if self.is_deployed():
            return self.contract_address
        else:
            self.deploy()
            return self.contract_address

    def _deposit(self):
        from brownie.project.BrownieProject import MimicMixingService

        self.require_deployed()
        deposited = MimicMixingService.at(self.contract_address).deposit({
            'from':
            accounts[0],
            'value':
            1000000000000000000
        })
        # print(deposited)
        return deposited

    def deposit(self, sender, amount):
        from brownie.project.BrownieProject import MimicMixingService

        print(
            f"sender: {sender} depositing {amount} at {self.contract_address}")

        self.require_deployed()
        deposited = MimicMixingService.at(self.contract_address).deposit({
            'from':
            sender,
            'value':
            amount
        })

        return deposited

    def withdraw(self, dispossable_address, amount):
        from brownie.project.BrownieProject import MimicMixingService
        self.require_deployed()
        # dispossable_address = accounts.add()
        # TODO: `from` should be the admin address
        sender = MimicMixingService.at(self.contract_address)
        withdrawn = MimicMixingService.at(
            self.contract_address).withdrawToDisposable(
                dispossable_address, amount, {'from': accounts[0]})

        return withdrawn
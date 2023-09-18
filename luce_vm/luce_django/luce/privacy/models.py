from django.db import models
from brownie import accounts


class MimicMixingServiceContract(models.Model):
    """
    Model to store the MimicMixingService contract address.
    """
    contract_address = models.CharField(max_length=42, null=True, blank=True)

    # contract_abi = models.TextField(null=True, blank=True)
    # contract_bytecode = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.contract_address

    def deploy(self):
        """
        Function to deploy the MimicMixingService contract.
        """
        # from brownie import accounts, MimicMixingService
        from brownie.project.BrownieProject import MimicMixingService

        deployed = MimicMixingService.deploy({'from': accounts[0]})
        self.contract_address = deployed.address

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

    def deposit(self):
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
        # pass

    def withdraw(self, dispossable_address, amount):
        from brownie.project.BrownieProject import MimicMixingService
        self.require_deployed()
        # dispossable_address = accounts.add()
        withdrawn = MimicMixingService.at(
            self.contract_address).withdrawToDisposable(
                dispossable_address, amount, {'from': accounts[0]})

        return withdrawn
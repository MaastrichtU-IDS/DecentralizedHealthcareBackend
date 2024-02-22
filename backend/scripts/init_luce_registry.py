import os
from brownie import accounts
from brownie import project, network
import django



p = project.load("brownie", name="BrownieProject")
p.load_config()
network.connect('luce')

from brownie.project.BrownieProject import LUCERegistry

DJANGO_SETTINGS_MODULE = 'lucehome.settings'
os.environ['DJANGO_SETTINGS_MODULE'] = DJANGO_SETTINGS_MODULE
django.setup()

# account[0] as the administrator
contract = LUCERegistry.deploy({'from': accounts[0]})
receipt = contract.tx
if receipt.status == 1:
    contract_address = receipt.contract_address
    print("Deploy LUCERegistry contract succeeded")
else:
    print("Deploy LUCERegistry contract failed")

print(contract_address)
print(receipt.status)

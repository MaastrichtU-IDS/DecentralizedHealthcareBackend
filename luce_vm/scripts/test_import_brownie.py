from brownie import project
from brownie import run
from brownie import network
from brownie import accounts

p = project.load("../brownie")
p.load_config()
network.connect()

# run("scripts/deploy_LUCERegistry.py")
# print(dict(p))

p.LUCERegistry.deploy({'from':accounts[0]})
# print(len(p.LUCERegistry))
current_contract = len(p.LUCERegistry) - 1

# print(p.LUCERegistry[current_contract].newDataProvider)

p.LUCERegistry[current_contract].newDataProvider(accounts[1], {'from': accounts[0]})

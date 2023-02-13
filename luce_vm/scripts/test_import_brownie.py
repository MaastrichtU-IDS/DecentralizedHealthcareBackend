from brownie import project
from brownie import run
from brownie import network

p = project.load("../brownie")
p.load_config()
network.connect()

# run("scripts/deploy_LUCERegistry.py")
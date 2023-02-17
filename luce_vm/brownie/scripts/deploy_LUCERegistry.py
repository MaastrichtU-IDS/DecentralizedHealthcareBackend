# from brownie import *
from brownie import LUCERegistry, accounts

def main(_owner):
    
    _owner = accounts[0]
    result = LUCERegistry.deploy({"from": _owner})
    # print(type(result))
    print(dir(result))
    print(result.address)
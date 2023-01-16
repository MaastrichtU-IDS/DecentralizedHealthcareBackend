from brownie import *

def main():
    result = LUCERegistry.deploy({'from': accounts[0]})
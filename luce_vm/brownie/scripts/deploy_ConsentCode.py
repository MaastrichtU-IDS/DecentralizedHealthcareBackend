from brownie import *

def main(_owner):
    result = ConsentCode.deploy({"from": _owner})
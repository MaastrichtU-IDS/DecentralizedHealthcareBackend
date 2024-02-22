from brownie import *

class LUCEBlockchain(object):
    def __init__(self, project_path):
        _project = project.load(project_path)
        config = _project.load_config()
        network_status = network.connect()
    
    def Deploy_LUCERegistry(self, script_path, method_name, owner):
        run(script_path, method_name=method_name, args=(owner,))

    def Deploy_ConsentCode(self, script_path, method_name, owner):
        run(script_path,method_name=method_name, args=(owner,))

# TODO The relative path of brownie is ugly
luce_blockchain = LUCEBlockchain("../../../../../brownie")

# TODO we can create a configure file to set the script path for smart contract
# luce_blockchain.Deploy_LUCERegistry("scripts/deploy_LUCERegistry.py","main", accounts[0])
luce_blockchain.Deploy_ConsentCode("scripts/deploy_ConsentCode.py", "main", accounts[0])
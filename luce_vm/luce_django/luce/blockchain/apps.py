from django.apps import AppConfig
from pathlib import Path


class BlockchainConfig(AppConfig):
    name = 'blockchain'

    def ready(self):
        from brownie import network, project
        brownie_folder = Path(__file__).parent.parent.parent.parent
        # print("Brownie folder: " + str(brownie_folder))
        brownie_path = brownie_folder / 'brownie'
        # print("Brownie path: " + str(brownie_path))
        # print("Loading Brownie from: " + str(brownie_path))

        p = project.load(brownie_path, name="BrownieProject")
        p.load_config()
        # print(p.dict())

        network.connect('luce')
        is_connected = network.is_connected()
        # print("Is connected: " + str(is_connected))

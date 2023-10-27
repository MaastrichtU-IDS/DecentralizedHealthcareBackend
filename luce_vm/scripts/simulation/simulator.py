# Standard libraries
import sys
import os
import json
import urllib3
from abc import ABC, abstractmethod

# Third-party libraries
import django
import networkx as nx
import matplotlib.pyplot as plt

from web3 import Web3

w3 = Web3(Web3.HTTPProvider('HTTP://127.0.0.1:7545'))

# Constants
LUCE_DJANGO_PATH = os.path.abspath(os.path.join('../..', 'luce_django/luce'))
DJANGO_SETTINGS_MODULE = 'lucehome.settings'


def setup_django():
    sys.path.insert(0, LUCE_DJANGO_PATH)
    os.environ['DJANGO_SETTINGS_MODULE'] = DJANGO_SETTINGS_MODULE
    django.setup()


setup_django()
# Local modules
from generate_user import generate_users
from generate_user import generate_data_requesters
from accounts.models import User


class Simulator:
    def __init__(self, num_of_users, num_of_requesters=0, strategy=None):
        self.http = urllib3.PoolManager()
        self.urls = {
            "login": "http://127.0.0.1:8000/user/login/",
            "register": "http://localhost:8000/user/register/",
            "upload_data": "http://localhost:8000/contract/dataUpload/",
            "deploy_registry": "http://localhost:8000/admin/deployRegistry/",
            "access_data": "http://localhost:8000/contract/requestAccess/"
        }

        self.user = generate_users(num_of_users)
        # exclude admin user
        self.requester = generate_data_requesters(num_of_users)
        self.directed_graph = nx.DiGraph()
        self.directed_graph_blockchain = nx.DiGraph()
        self.strategy = strategy
        self.provider = []

    def set_strategy(self, strategy):
        self.strategy = strategy

    def run(self):
        if self.strategy:
            self.strategy.execute(self)
        else:
            print("No strategy set.")

    def _login(self, url, user):
        encoded_user = json.dumps(user).encode('utf-8')
        r = self.http.request('POST',
                              self.urls['login'],
                              body=encoded_user,
                              headers={'Content-Type': 'application/json'})

        token = json.loads(r.data.decode('utf-8'))["data"]["token"]
        return token

    def register_requesters(self):
        for requester in self.requester['requesters']:
            email = requester['registration_data']['email']
            print("Register requester: " + email)
            self._register(self.urls['register'],
                           requester['registration_data'])

    def register_users(self):
        for user in self.user['users']:
            email = user['registration_data']['email']
            print("Register user: " + email)
            self._register(self.urls['register'], user['registration_data'])

    def _register(self, registration_url, registration_data):
        r = self.http.request(
            'POST',
            self.urls['register'],
            body=json.dumps(registration_data).encode('utf-8'),
            headers={'Content-Type': 'application/json'})

        result = json.loads(r.data.decode('utf-8'))

    def _get_all_provider(self):
        providers = User.objects.filter(user_type=0)
        return providers

    def _get_all_datasets(self):
        p = self._get_all_provider()
        print(p)
        # pass

    def _access_data(self, access_url, access_data, token):
        d = json.dumps(access_data).encode('utf-8')

        r = self.http.request('POST',
                              self.urls['access_data'],
                              body=d,
                              headers={
                                  'Content-Type': 'application/json',
                                  'Authorization': 'Token ' + token
                              })

        result = json.loads(r.data.decode('utf-8'))
        # print(result)
        print("Access data result: " + str(result))
        return result

    def access_data(self):
        for requester in self.requester['requesters']:
            email = requester['registration_data']['email']
            print("Access data for requester: " + email)
            token = self._login(
                self.urls['login'], {
                    'username': email,
                    'password': requester['registration_data']['password']
                })
            user_instance = User.objects.get(email=email)
            user_address = user_instance.ethereum_public_key

            for provider in self.provider:
                access_data = requester['access_data']
                access_data['dataset_addresses'] = provider['dataset']

                # add edge to graph
                for data in provider['dataset']:
                    # print(f"Provider {provider['user']}'s data: " + data)
                    # print(f"Requester {email}'s address: " + user_address)
                    node_from = self._address_to_label(user_address, 1)
                    self.directed_graph.add_node(node_from,
                                                 address=user_address,
                                                 type="r")

                    node_to = self._address_to_label(data)
                    self.directed_graph.add_node(node_to,
                                                 address=data,
                                                 type="d")

                    self.directed_graph.add_edge(node_from, node_to)

                print(f"{email} access {provider['user']}'s data")
                self._access_data(self.urls['access_data'], access_data, token)

    def upload_data(self):
        for user in self.user['users']:
            email = user['registration_data']['email']
            print("Upload data for user: " + email)
            token = self._login(
                self.urls['login'], {
                    'username': email,
                    'password': user['registration_data']['password']
                })
            user_instance = User.objects.get(email=email)
            user_address = user_instance.ethereum_public_key

            uploaded = self._upload_data(self.urls['upload_data'],
                                         user['uploaded_data'], token)

            uploaded_contract_address = uploaded['data']['contracts'][
                "contract_address"]

            provier_with_dataset = {
                "user": email,
                "address": user_address,
                "dataset": [uploaded_contract_address]
            }

            self.provider.append(provier_with_dataset)
            print(f"User {email} address: " + user_address)
            # print(self._address_to_label(user_address, 0))
            print(f"User {email} uploaded data: " + uploaded_contract_address)
            # print(self._address_to_label(uploaded_contract_address))

            node_from = self._address_to_label(user_address, 0)
            node_to = self._address_to_label(uploaded_contract_address)

            self.directed_graph.add_node(node_from,
                                         address=user_address,
                                         type="p")
            self.directed_graph.add_node(node_to,
                                         address=uploaded_contract_address,
                                         type="d")

            self.directed_graph.add_edge(node_from, node_to)

    def _upload_data(self, upload_url, data, token):
        d = json.dumps(data).encode('utf-8')

        r = self.http.request('POST',
                              self.urls['upload_data'],
                              body=d,
                              headers={
                                  'Content-Type': 'application/json',
                                  'Authorization': 'Token ' + token
                              })

        result = json.loads(r.data.decode('utf-8'))
        return result

    def deploy_registry(self):
        admin = self.user['users'].pop()
        admin_token = self._login(
            self.urls['login'], {
                'username': admin['registration_data']['email'],
                'password': admin['registration_data']['password']
            })
        self._deploy_registry(admin_token)

    def _deploy_registry(self, admin_token):
        print("Deploy registry")
        r = self.http.request("POST",
                              self.urls['deploy_registry'],
                              headers={
                                  'Content-Type': 'application/json',
                                  'Authorization': 'Token ' + admin_token
                              })
        result = json.loads(r.data.decode('utf-8'))

    def _address_to_label(self, address, type=-1):
        """
        type: 0 - provider, 1 - requester
        """
        if type == 0:
            return "p:" + address[:5] + "..." + address[-5:]
        elif type == 1:
            return "r:" + address[:5] + "..." + address[-5:]
        else:
            return address[:5] + "..." + address[-5:]

    def _clear_data(self):
        User.objects.all().delete()

    def _draw_graph(self, name="graph.png"):
        # layout = nx.spring_layout(self.directed_graph)
        nx.draw(self.directed_graph, with_labels=True)
        plt.show()

    def _save_graph(self, name="graph.png"):
        # layout = nx.spring_layout(self.directed_graph)
        nx.draw(self.directed_graph, with_labels=True)
        img = f'images/{name}'
        plt.savefig(img)
        plt.close()

    def _analyze_graph(self):
        nodes = self.directed_graph.nodes()
        # print(nodes.data())
        dataset_address = ""
        for node in nodes.data():
            if node[1]['type'] == 'd':
                dataset_address = node[1]['address']
                break

        latest_txs_64 = self._get_txs_latest()

        for tx in latest_txs_64:
            tx_hash = w3.toHex(tx['hash'])
            receipt = w3.eth.get_transaction_receipt(tx_hash)
            # print(receipt)
            if receipt['to'] == dataset_address:
                node_from = self._address_to_label(receipt['from'])
                node_to = self._address_to_label(receipt['to'])
                self.directed_graph_blockchain.add_node(
                    node_from, address=receipt['from'])
                self.directed_graph_blockchain.add_node(node_to,
                                                        address=receipt['to'])
                self.directed_graph_blockchain.add_edge(node_from, node_to)

                # print(receipt)
        nx.draw(self.directed_graph_blockchain, with_labels=True)
        plt.show()

    def _get_txs_latest(self, num=64):

        latest_block_number = w3.eth.block_number
        print("latest block number: ", latest_block_number)

        all_txs = []
        for block_number in range(latest_block_number - num,
                                  latest_block_number + 1):
            print("retrieve block: ", block_number)
            block = w3.eth.get_block(block_number, full_transactions=True)
            for tx in block.transactions:
                all_txs.append(tx)

        return all_txs

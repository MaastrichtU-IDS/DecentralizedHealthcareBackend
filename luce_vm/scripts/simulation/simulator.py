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
            "deploy_registry": "http://localhost:8000/admin/deployRegistry/"
        }

        self.user = generate_users(num_of_users)
        self.requester = generate_data_requesters(num_of_users)
        self.directed_graph = nx.DiGraph()
        self.strategy = strategy

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
        pass

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
            self.directed_graph.add_edge(
                self._address_to_label(user_address),
                self._address_to_label(
                    uploaded['data']['contracts']["contract_address"]))

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

    def _address_to_label(self, address):
        return address[:5] + "..." + address[-5:]

    def _clear_data(self):
        User.objects.all().delete()

    def _draw_graph(self):
        nx.draw(self.directed_graph, with_labels=True)
        plt.show()

import urllib3
import json

import sys
import os
import django

from generate_user import generate_users

luce_django_path = os.path.abspath('../..')  # luce_vm
luce_django_path = os.path.join(luce_django_path, 'luce_django/luce')
sys.path.insert(0, luce_django_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'lucehome.settings'
django.setup()

from accounts.models import User

import networkx as nx
import matplotlib.pyplot as plt


class Simulator:
    def __init__(self, num_of_users):
        self.http = urllib3.PoolManager()
        self.urls = {
            "login": "http://127.0.0.1:8000/user/login/",
            "register": "http://localhost:8000/user/register/",
            "upload_data": "http://localhost:8000/contract/dataUpload/",
            "deploy_registry": "http://localhost:8000/admin/deployRegistry/"
        }

        self.user = generate_users(num_of_users)
        self.directed_graph = nx.DiGraph()

        self.switcher = {1: self._senario_1}

    def run(self, senario_num):
        self.switcher.get(senario_num, lambda: "Invalid senario")()

    def _login(self, url, user):
        encoded_user = json.dumps(user).encode('utf-8')
        r = self.http.request('POST',
                              self.urls['login'],
                              body=encoded_user,
                              headers={'Content-Type': 'application/json'})

        token = json.loads(r.data.decode('utf-8'))["data"]["token"]
        return token

    def _register(self, registration_url, registration_data):
        r = self.http.request(
            'POST',
            self.urls['register'],
            body=json.dumps(registration_data).encode('utf-8'),
            headers={'Content-Type': 'application/json'})

        result = json.loads(r.data.decode('utf-8'))
        # print(result)
        return result

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
        # print(result)
        return result

    def _deploy_registry(self, url, admin_token):
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

    def _senario_1(self):
        print("Start simulate senario 1")
        # print(self.user)

        # 1. clear user data
        User.objects.all().delete()

        # 2. register users
        for user in self.user['users']:
            email = user['registration_data']['email']
            print("Register user: " + email)
            self._register(self.urls['register'], user['registration_data'])

        # 3. deploy registry
        admin = self.user['users'].pop()
        admin_token = self._login(
            self.urls['login'], {
                'username': admin['registration_data']['email'],
                'password': admin['registration_data']['password']
            })
        self._deploy_registry(self.urls['deploy_registry'], admin_token)

        # 4. upload data
        print("Upload data:")
        for user in self.user['users']:
            # 4.1 login
            token = self._login(
                self.urls['login'], {
                    'username': user['registration_data']['email'],
                    'password': user['registration_data']['password']
                })

            email = user['registration_data']['email']
            user_instance = User.objects.get(email=email)
            user_address = user_instance.ethereum_public_key

            # 4.2 upload data
            uploaded = self._upload_data(self.urls['upload_data'],
                                         user['uploaded_data'], token)
            print("Upload data for user: " + email)
            uploaded_address = uploaded['data']['contracts']
            print("Uploaded address: ")
            print(uploaded_address['contract_address'])
            self.directed_graph.add_edge(
                self._address_to_label(user_address),
                self._address_to_label(uploaded_address['contract_address']))

        nx.draw(self.directed_graph, with_labels=True)
        plt.show()


s = Simulator(3)
s.run(1)
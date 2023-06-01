import urllib3
import json

import sys
import os
import django

# BASE_DIR = "../../luce_django/luce"

# sys.path.append("../../luce_django/luce")
# from accounts.models import User

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', "lucehome.settings")
# # django.setup()

# from accounts.models import User

http = urllib3.PoolManager()

registration_data = {
    "last_name": "piccini",
    "email": "email90@email.com",
    "password": "password123",
    "create_wallet": True,
    "user_type": 0
}

user = {
    "username": registration_data["email"],
    "password": registration_data["password"]
}

url = "http://127.0.0.1:8000/user/login/"


def Login(url, user):
    encoded_user = json.dumps(user).encode('utf-8')
    r = http.request('POST',
                     url,
                     body=encoded_user,
                     headers={'Content-Type': 'application/json'})

    token = json.loads(r.data.decode('utf-8'))["data"]["token"]
    return token


registration_url = "http://localhost:8000/user/register/"


def Register(registration_url, registration_data):
    r = http.request('POST',
                     registration_url,
                     body=json.dumps(registration_data).encode('utf-8'),
                     headers={'Content-Type': 'application/json'})

    result = json.loads(r.data.decode('utf-8'))
    print(result)
    return result


# Register(registration_url, registration_data)
# token = Login(url, user)
# print(token)

uploaded_data = {
    "estimate": False,
    "description": "ds",
    "link": "http://link.com",
    "no_restrictions": False,
    "open_to_general_research_and_clinical_care": False,
    "open_to_HMB_research": False,
    "open_to_population_and_ancestry_research": False,
    "open_to_disease_specific": False
}
upload_data_url = "http://localhost:8000/contract/dataUpload/"


def UploadData(upload_url, data, token):
    d = json.dumps(data).encode('utf-8')

    r = http.request('POST',
                     upload_data_url,
                     body=d,
                     headers={
                         'Content-Type': 'application/json',
                         'Authorization': 'Token ' + token
                     })

    result = json.loads(r.data.decode('utf-8'))
    print(result)


deploy_registry_url = "http://localhost:8000/admin/deployRegistry/"


def DeployRegistry(url, admin_token):
    r = http.request("POST",
                     url,
                     headers={
                         'Content-Type': 'application/json',
                         'Authorization': 'Token ' + admin_token
                     })

    result = json.loads(r.data.decode('utf-8'))
    print(result)


# UploadData(upload_data_url, uploaded_data)

test_url = "http://localhost:8000/"
def Test(url):
    r = http.request("GRT", url)
    result = json.loads(r.data.decode('utf-8'))
    print(result)


def pipeline():

    # Test(test_url)
    # return 
    print("Start simulation")
    # return
    
    # 1. clear user data
    # User.objects.all().delete()

    # 2. load faked user data
    with open("faked_data.json", "r") as f:
        data = json.load(f)

    users = data['users']

    # 3. register users
    for user in users:
        Register(registration_url, user['registration_data'])

    # 4. deploy registry
    admin = users.pop()
    admin_token = Login(
        url, {
            'username': admin['registration_data']['email'],
            'password': admin['registration_data']['password']
        })
    DeployRegistry(deploy_registry_url, admin_token)

    # return

    # 4. upload data
    print("Upload data:")
    for user in users:
        # 4.1 login
        token = Login(
            url, {
                'username': user['registration_data']['email'],
                'password': user['registration_data']['password']
            })
        print(token)
        # 4.2 upload data
        UploadData(upload_data_url, user['uploaded_data'], token)


pipeline()
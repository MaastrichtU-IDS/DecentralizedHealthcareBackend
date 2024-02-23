import os
import sys
import django
import copy
import json
import urllib3
from brownie import project, network, accounts

# Constants
LUCE_DJANGO_PATH = os.path.abspath(os.path.join('..', 'luce_django/luce'))
DJANGO_SETTINGS_MODULE = 'lucehome.settings'
BROWNIE_PROJECT_PATH = os.path.abspath(os.path.join('..', 'brownie'))
http = urllib3.PoolManager()

user_template = {
    "registration_data": {
        "last_name": "bob",
        "email": "bob@email.com",  # login field
        "password": "passwordbob",  # login field
        "create_wallet": True,
        "user_type": 0
    },
    "uploaded_data": {
        "estimate": False,
        "description": "description",
        "link": "http://link.com",
        "no_restrictions": False,
        "open_to_general_research_and_clinical_care": False,
        "open_to_HMB_research": False,
        "open_to_population_and_ancestry_research": False,
        "open_to_disease_specific": False
    },
    "access_data": {
        "estimate": False,
        "dataset_addresses": ["0x0000"],
        "general_research_purpose": {
            "use_for_methods_development": True,
            "use_for_reference_or_control_material": True,
            "use_for_populations_research": True,
            "use_for_ancestry_research": True,
            "use_for_HMB_research": True
        },
        "HMB_research_purpose": {
            "use_for_research_concerning_fundamental_biology": False,
            "use_for_research_concerning_genetics": False,
            "use_for_research_concerning_drug_development": False,
            "use_for_research_concerning_any_disease": False,
            "use_for_research_concerning_age_categories": False,
            "use_for_research_concerning_gender_categories": False
        },
        "clinical_purpose": {
            "use_for_decision_support": False,
            "use_for_disease_support": False
        }
    }
}


def setup_django():
    # to load same settings as in container
    os.environ['DJANGO_USE_PSQL'] = 'true'
    os.environ['SIMULATION'] = 'true'
    sys.path.insert(0, LUCE_DJANGO_PATH)
    os.environ['DJANGO_SETTINGS_MODULE'] = DJANGO_SETTINGS_MODULE
    django.setup()


def setup_brownie():
    p = project.load(BROWNIE_PROJECT_PATH)
    p.load_config()
    network.connect()
    return p


def generate_user(user_id):
    user = copy.deepcopy(user_template)

    last_name = "bob" + str(user_id)
    email = last_name + "@email.com"
    password = "password" + last_name
    create_wallet = True
    user_type = 0
    user['registration_data']['last_name'] = last_name
    user['registration_data']['email'] = email
    user['registration_data']['password'] = password
    user['registration_data']['create_wallet'] = create_wallet
    user['registration_data']['user_type'] = user_type

    estimate = False
    description = 'description'
    link = 'http://link.com'
    user['uploaded_data']["estimate"] = estimate
    user["uploaded_data"]['description'] = description
    user['uploaded_data']['link'] = link

    return user.copy()


urls = {
    "login": "http://127.0.0.1:8000/user/login/",
    "register": "http://localhost:8000/user/register/",
    "upload_data": "http://localhost:8000/contract/dataUpload/",
    "deploy_registry": "http://localhost:8000/admin/deployRegistry/",
    "access_data": "http://localhost:8000/contract/requestAccess/"
}


def register_user(url, user):
    encoded_user = json.dumps(user).encode('utf-8')
    r = http.request('POST',
                     #  urls['register'],
                     url,
                     body=encoded_user,
                     headers={'Content-Type': 'application/json'})
    # print(r.data)


def login(url, login_data):

    encoded_user = json.dumps(login_data).encode('utf-8')

    r = http.request('POST',
                     #  urls['login'],
                     url,
                     body=encoded_user,
                     headers={'Content-Type': 'application/json'})

    token = json.loads(r.data.decode('utf-8'))["data"]["token"]
    return token


def deploy_registry():
    user = generate_user(0)
    # print(user)
    register_data = user['registration_data']
    register_user(urls['register'], register_data)

    login_data = {
        'username': user['registration_data']['email'],
        'password': user['registration_data']['password'],
    }
    token = login(urls['login'], login_data)
    r = http.request('POST',
                     urls['deploy_registry'],
                     headers={'Authorization': 'Token ' + token})
    # print(r.data)


deploy_registry()

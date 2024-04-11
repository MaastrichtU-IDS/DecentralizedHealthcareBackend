# import os
# from brownie import accounts
# from brownie import project, network
# import django
import urllib3
import json

http = urllib3.PoolManager()

registration_data = {
    "last_name":"piccini",
    "email":"vincent.emonet@gmail.com",
    "password":"password",
    "create_wallet":True,
    "user_type":0
}

user = {
    "username": registration_data["email"],
    "password": registration_data["password"]
}

url = "http://localhost:8000/user/login/"

def login(url, user):
    encoded_user = json.dumps(user).encode('utf-8')
    r = http.request(
        'POST',
        url,
        body=encoded_user,
        headers={
            'Content-Type': 'application/json'
        }
    )
    print(r.data.decode('utf-8'))
    token = json.loads(r.data.decode('utf-8'))["data"]["token"]
    return token

# registration_url = "http://localhost:8000/user/register/"
# def Register(registration_url, registration_data):
#     r = http.request(
#         'POST',
#         registration_url,
#         body=json.dumps(registration_data).encode('utf-8'),
#         headers={
#             'Content-Type':'application/json'
#         }
#     )
#     result = json.loads(r.data.decode('utf-8'))
#     # print(result)
#     return result
# Register(registration_url, registration_data)


token = login(url, user)
print(token)

d = json.dumps({
    "estimate": False,
}).encode('utf-8')
r = http.request(
    'POST',
    "http://localhost:8000/admin/deployRegistry/",
    body=d,
    headers={
        'Content-Type':'application/json',
        'Authorization': 'Token ' + token
    }
)
print(r.data.decode('utf-8'))
# result = json.loads(r.data.decode('utf-8'))
# print(result)



# uploaded_data = {
#     "estimate":False,
#     "description":"ds",
#     "link":"http://link.com",
#     "no_restrictions":False,
#     "open_to_general_research_and_clinical_care":False,
#     "open_to_HMB_research":False,
#     "open_to_population_and_ancestry_research":False,
#     "open_to_disease_specific":False
# }
# upload_data_url = "http://localhost:8000/contract/dataUpload/"
# def upload_data(upload_url, data):
#     d = json.dumps(data).encode('utf-8')

#     r = http.request('POST', upload_data_url, body=d, headers={
#         'Content-Type':'application/json',
#         'Authorization': 'Token ' + token
#     })

#     result = json.loads(r.data.decode('utf-8'))
#     print(result)

# UploadData(upload_data_url, uploaded_data)



# p = project.load("brownie", name="BrownieProject")
# p.load_config()
# network.connect('luce')

# from brownie.project.BrownieProject import LUCERegistry

# DJANGO_SETTINGS_MODULE = 'lucehome.settings'
# os.environ['DJANGO_SETTINGS_MODULE'] = DJANGO_SETTINGS_MODULE
# django.setup()

# # account[0] as the administrator
# contract = LUCERegistry.deploy({'from': accounts[0]})
# receipt = contract.tx
# if receipt.status == 1:
#     contract_address = receipt.contract_address
#     print("Deploy LUCERegistry contract succeeded")
# else:
#     print("Deploy LUCERegistry contract failed")

# print(contract_address)
# print(receipt.status)

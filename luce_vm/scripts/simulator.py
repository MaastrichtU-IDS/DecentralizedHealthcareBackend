import urllib3
import json

http = urllib3.PoolManager()

registration_data = {   
    "last_name":"piccini",
    "email":"email90@email.com",
    "password":"password123",
    "create_wallet":True,
    "user_type":0
}

user = {
    "username": registration_data["email"],
    "password": registration_data["password"]
}

url = "http://127.0.0.1:8000/user/login/"


def Login(url, user):
    encoded_user = json.dumps(user).encode('utf-8')
    r = http.request(
        'POST',
        url,
        body=encoded_user,
        headers={
            'Content-Type': 'application/json'
        }

    )

    token = json.loads(r.data.decode('utf-8'))["data"]["token"]
    return token



registration_url = "http://localhost:8000/user/register/"
def Register(registration_url, registration_data):
    r = http.request(
        'POST', 
        registration_url, 
        body=json.dumps(registration_data).encode('utf-8'),
        headers={
            'Content-Type':'application/json'
        }
    )

    result = json.loads(r.data.decode('utf-8'))
    # print(result)
    return result



# Register(registration_url, registration_data)
token = Login(url, user)
# print(token)

uploaded_data = {   
    "estimate":False,
    "description":"ds",
    "link":"http://link.com",
    "no_restrictions":False,
    "open_to_general_research_and_clinical_care":False,
    "open_to_HMB_research":False,
    "open_to_population_and_ancestry_research":False,
    "open_to_disease_specific":False
}
upload_data_url = "http://localhost:8000/contract/dataUpload/"
def UploadData(upload_url, data):
    d = json.dumps(data).encode('utf-8')

    r = http.request('POST', upload_data_url, body=d, headers={
        'Content-Type':'application/json',
        'Authorization': 'Token ' + token
    })

    result = json.loads(r.data.decode('utf-8'))
    print(result)

# UploadData(upload_data_url, uploaded_data)
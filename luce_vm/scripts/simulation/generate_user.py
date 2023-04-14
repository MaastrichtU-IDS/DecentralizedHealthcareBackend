import json
import copy

user_template = {
    "registration_data": {
        "last_name": "bob",
        "email": "bob@email.com",  # login field
        "password": "passwordbob",  #login field
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
    }
}


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


def generate_users(number):
    data = {"users": []}
    all_users = []
    for i in range(number):
        new_user = generate_user(i)
        all_users.append(new_user.copy())

    data['users'] = all_users

    return data


users = generate_users(3)

with open("faked_data.json", "w") as f:
    json.dump(users, f)

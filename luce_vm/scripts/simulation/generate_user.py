import json
import copy
"""
At the beginning of deployment, we did not take into account the type of user; However, we have different types of users now; 
thus, while discussing data provider, we just use user; and for other user types, we should indicate the type of user
"""
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


def generate_a_data_requester(requester_id):
    requester = copy.deepcopy(user_template)
    last_name = "alice" + str(requester_id)
    email = last_name + "@email.com"
    password = "password" + last_name
    create_wallet = True
    user_type = 1
    requester['registration_data']['last_name'] = last_name
    requester['registration_data']['email'] = email
    requester['registration_data']['password'] = password
    requester['registration_data']['create_wallet'] = create_wallet
    requester['registration_data']['user_type'] = user_type

    return requester.copy()


def generate_data_requesters(number):
    data = {"requesters": []}
    all_requesters = []
    for i in range(number):
        new_requester = generate_a_data_requester(i)
        all_requesters.append(new_requester.copy())

    data['requesters'] = all_requesters

    return data


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


users = generate_users(10)

with open("faked_data.json", "w") as f:
    json.dump(users, f)

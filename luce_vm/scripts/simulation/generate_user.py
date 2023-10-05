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
    },
    "access_data": {
        "estimate": false,
        "dataset_addresses": ["0x0000"],
        "general_research_purpose": {
            "use_for_methods_development": true,
            "use_for_reference_or_control_material": true,
            "use_for_populations_research": true,
            "use_for_ancestry_research": true,
            "use_for_HMB_research": true
        },
        "HMB_research_purpose": {
            "use_for_research_concerning_fundamental_biology": false,
            "use_for_research_concerning_genetics": false,
            "use_for_research_concerning_drug_development": false,
            "use_for_research_concerning_any_disease": false,
            "use_for_research_concerning_age_categories": false,
            "use_for_research_concerning_gender_categories": false
        },
        "clinical_purpose": {
            "use_for_decision_support": false,
            "use_for_disease_support": false
        }
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


users = generate_users(10)

with open("faked_data.json", "w") as f:
    json.dump(users, f)

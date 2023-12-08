from accounts.models import User
from blockchain.models import ResearchPurpose
from blockchain.models import Restrictions
from blockchain.models import ConsentContract


def create_user():
    user = User.objects.create_user(
        email='exmaple@test.com',
        password='testpassword',
        first_name='test',
        last_name='user',
        age=20,
        gender='M'
    )

    user.create_wallet()

    return user


def create_research_purpose():
    return ResearchPurpose.objects.create()


def create_restrictions():
    return Restrictions.objects.create(
        no_restrictions=True,
        open_to_general_research_and_clinical_care=False,
        open_to_HMB_research=False,
        open_to_population_and_ancestry_research=False,
        open_to_disease_specific=False,
    )


def create_consent_contract(user, research_purpose, restrictions):
    return ConsentContract.objects.create(
        contract_address='0xSomeAddress',
        user=user,
        research_purpose=research_purpose,
        restrictions=restrictions
    )

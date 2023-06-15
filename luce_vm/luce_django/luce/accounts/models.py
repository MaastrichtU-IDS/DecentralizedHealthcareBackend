# accounts.models.py

from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from django.core.validators import MaxValueValidator, MinValueValidator
import utils.web3_scripts as web3
from django.dispatch import receiver

from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)
from django.conf import settings

# from brownie import LUCERegistry
from brownie import project
from brownie import network
from brownie import accounts
import urllib3
import json
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

from utils.utils import get_initial_response, set_logger

import os

logger = set_logger(__file__)

# project should be loaded at somewhere else
loaded_project = project.get_loaded_projects()

if len(loaded_project) == 0:
    print("No project")
else:
    for p in loaded_project:
        p.close()

LUCE_PROJECT_PATH = os.path.join(settings.BASE_DIR, "../../brownie")
# print(luce_project_path)
print(LUCE_PROJECT_PATH)
luce_project = project.load(LUCE_PROJECT_PATH)
luce_project.load_config()
# print("network.show_active()")
print(network.is_connected())
network.connect()
print(network.is_connected())



class Verifier(models.Model):
    address = models.CharField(max_length=255, null=True)

    def deploy(self):
        private_key = "56c6de6fd54438dbb31530f5fdeeaada0b1517880c91dfcd46a4e5fec59a9c79"
        new_account = accounts.add(private_key=private_key)
        contract = luce_project.PlonkVerifier.deploy({'from': new_account})

        self.address = contract.address
        self.save()


class UserManager(BaseUserManager):
    def create_user(self,
                    email,
                    gender,
                    age,
                    first_name,
                    last_name,
                    password,
                    user_type=None,
                    ethereum_private_key=None,
                    ethereum_public_key=None,
                    contract_address=None,
                    is_staff=False,
                    is_admin=False):
        """
        Creates and saves a User with the given arguments and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        if not first_name:
            raise ValueError('Users must have a first_name')
        if not last_name:
            raise ValueError('Users must have a last_name')
        if not password:
            raise ValueError('Users must have a password')

        user = self.model(email=self.normalize_email(email), )

        user.gender = gender
        user.staff = is_staff
        user.set_password(password)
        user.first_name = first_name
        user.last_name = last_name
        user.admin = is_admin
        user.ethereum_private_key = ethereum_private_key
        user.ethereum_public_key = ethereum_public_key
        user.user_type = user.user_type
        user.save(using=self._db)
        user.contract_address = contract_address
        user.age = age
        return user

    def create_staffuser(self, email, first_name, last_name, password):
        """
        Creates and saves a staff user.
        """
        user = self.create_user(
            email,
            first_name,
            last_name,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        email,
        first_name,
        last_name,
        password,
        ethereum_public_key="0x43e196c418b4b7ebf71ba534042cc8907bd39dc9",
        ethereum_private_key="0x5714ad5f65fb27cb0d0ab914db9252dfe24cf33038a181555a7efc3dcf863ab3"
    ):
        """
        Creates and saves a superuser.
        """
        user = self.create_user(
            email,
            first_name,
            last_name,
            password=password,
            ethereum_public_key="0x43e196c418b4b7ebf71ba534042cc8907bd39dc9",
            ethereum_private_key=
            "0x5714ad5f65fb27cb0d0ab914db9252dfe24cf33038a181555a7efc3dcf863ab3"
        )
        user.staff = True
        user.admin = True
        user.user_type = 3
        user.save(using=self._db)
        return user

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_auth_token(sender, instance=None, created=False, **kwargs):
        if created:
            Token.objects.create(user=instance)


# Our custom user class
class User(AbstractBaseUser):
    # id,
    # password and
    # last_login are automatically inherited AbstractBaseUser
    # The other model fields we define ourselves
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    country = models.CharField(max_length=25, null=True)

    institution = models.CharField(max_length=255, null=True)

    ethereum_private_key = models.CharField(max_length=255,
                                            blank=True,
                                            null=True)

    ethereum_public_key = models.CharField(max_length=255,
                                           blank=True,
                                           null=True)

    # Make these fields compulsory?
    first_name = models.CharField(max_length=255, blank=True, null=True)

    last_name = models.CharField(max_length=255, blank=True, null=True)

    # Can use this later to activate certain features only
    # once ethereum address is associated
    # True for now while developing..
    is_approved = models.BooleanField(default=True, null=True, blank=True)

    # user_type is used to know if the user is a Data Provider(0) or a data requester(1)
    user_type = models.IntegerField(choices=[(0, "Data Provider"),
                                             (1, "Data Requester")],
                                    null=True)

    # active user? -> can login
    active = models.BooleanField(default=True)

    # a admin user; non super-user
    staff = models.BooleanField(default=False)

    # a superuser
    admin = models.BooleanField(default=False)

    # notice the absence of a "Password field", that's built in.

    # gender of the user
    gender = models.CharField(choices=[(0, 'Male'), (1, 'Female')],
                              max_length=6,
                              null=True)

    age = models.IntegerField(null=True)

    # Define which field should be the username for login
    USERNAME_FIELD = 'email'

    # USERNAME_FIELD & Password are required by default
    # Add additional required fields here:
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def create_wallet(self):
        # for simulation, we just create a new account for the user
        # and transfer some ether to them
        new_account = accounts.add()
        txn_receipt = accounts[0].transfer(new_account, 1e18)

        self.ethereum_public_key = new_account.address
        self.ethereum_private_key = new_account.private_key

        print(self.ethereum_public_key)
        # txn_receipt, account = web3.assign_address_v3()
        # self.ethereum_public_key = account.address
        # self.ethereum_private_key = account.privateKey.hex()
        return txn_receipt

    # The following default methods are expected to be defined by Django
    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True

    # Properties are based on our custom attributes
    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user an admin member?"
        return self.admin

    @property
    def is_active(self):
        "Is the user active?"
        return self.active


class Restrictions(models.Model):
    no_restrictions = models.BooleanField()
    open_to_general_research_and_clinical_care = models.BooleanField()
    open_to_HMB_research = models.BooleanField()
    open_to_population_and_ancestry_research = models.BooleanField()
    open_to_disease_specific = models.BooleanField()


class GeneralResearchPurpose(models.Model):
    use_for_methods_development = models.BooleanField(default=False)
    use_for_reference_or_control_material = models.BooleanField(default=False)
    use_for_research_concerning_populations = models.BooleanField(
        default=False)
    use_for_research_ancestry = models.BooleanField(default=False)
    use_for_biomedical_research = models.BooleanField(default=False)


class HMBResearchPurpose(models.Model):
    use_for_research_concerning_fundamental_biology = models.BooleanField(
        default=False)
    use_for_research_concerning_genetics = models.BooleanField(default=False)
    use_for_research_concerning_drug_development = models.BooleanField(
        default=False)
    use_for_research_concerning_any_disease = models.BooleanField(
        default=False)
    use_for_research_concerning_age_categories = models.BooleanField(
        default=False)
    use_for_research_concerning_gender_categories = models.BooleanField(
        default=False)


class ClinicalPurpose(models.Model):
    use_for_decision_support = models.BooleanField(default=False)
    use_for_disease_support = models.BooleanField(default=False)


class ResearchPurpose(models.Model):
    general_research_purpose = models.ForeignKey(GeneralResearchPurpose,
                                                 on_delete=models.CASCADE,
                                                 null=True)
    HMB_research_purpose = models.ForeignKey(HMBResearchPurpose,
                                             on_delete=models.CASCADE,
                                             null=True)
    clinical_purpose = models.ForeignKey(ClinicalPurpose,
                                         on_delete=models.CASCADE,
                                         null=True)


class ConsentContract(models.Model):
    contract_address = models.CharField(max_length=255, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restrictions = models.ForeignKey(Restrictions, on_delete=models.CASCADE)
    research_purpose = models.ForeignKey(ResearchPurpose,
                                         on_delete=models.CASCADE,
                                         null=True)

    def update_data_consent(self):
        transaction_dict = {
            'from': accounts.add(private_key=self.user.ethereum_private_key)
        }

        logger.info(self.user.ethereum_public_key)
        transaction_receipt = luce_project.ConsentCode.at(
            self.contract_address).UploadDataPrimaryCategory(
                self.user.ethereum_public_key,
                self.restrictions.no_restrictions,
                self.restrictions.open_to_general_research_and_clinical_care,
                self.restrictions.open_to_HMB_research,
                self.restrictions.open_to_population_and_ancestry_research,
                self.restrictions.open_to_disease_specific, transaction_dict)

        return transaction_receipt.status

    def upload_data_consent(self, estimate):
        return web3.upload_data_consent(self, estimate)

    def retrieve_contract_owner(self):
        return web3.retrieve_contract_owner(self)

    def deploy(self):
        private_key = self.user.ethereum_private_key
        new_account = accounts.add(private_key=private_key)
        contract = luce_project.ConsentCode.deploy({'from': new_account})

        self.contract_address = contract.address
        self.save()

    def deploy_contract(self):
        tx_receipt = web3.deploy_consent(self.user)
        if type(tx_receipt) is list:
            return tx_receipt
        self.contract_address = tx_receipt["contractAddress"]
        self.save()
        return tx_receipt

    def give_clinical_research_purpose(self, user, estimate):
        rp = self.research_purpose.clinical_purpose
        # print(rp)
        logger.info(rp)
        private_key = self.user.ethereum_private_key
        new_account = accounts.add(private_key=private_key)

        txn_dict = {'from': new_account}

        receipt = luce_project.ConsentCode.at(
            self.contract_address).giveClinicalPurpose(
                user.ethereum_public_key,
                rp.use_for_decision_support,
                rp.use_for_disease_support,
                txn_dict
        )

        logger.info(receipt)

        return receipt.status

        # tx = web3.give_clinical_research_purpose(self, user, estimate)
        # return tx

    def give_HMB_research_purpose(self, user, estimate):
        rp = self.research_purpose.HMB_research_purpose
        # print(rp)
        logger.info(rp)
        private_key = self.user.ethereum_private_key
        new_account = accounts.add(private_key=private_key)

        txn_dict = {'from': new_account}

        receipt = luce_project.ConsentCode.at(
            self.contract_address).giveHMBPurpose(
                user.ethereum_public_key, 
                rp.use_for_research_concerning_fundamental_biology,
                rp.use_for_research_concerning_genetics,
                rp.use_for_research_concerning_drug_development,
                rp.use_for_research_concerning_any_disease,
                rp.use_for_research_concerning_age_categories,
                rp.use_for_research_concerning_gender_categories,
                txn_dict
        )

        logger.info(receipt)
        return receipt.status
        # tx = web3.give_HMB_research_purpose(self, user, estimate)
        # return tx

    def give_general_research_purpose(self, user, estimate):
        rp = self.research_purpose.general_research_purpose
        private_key = self.user.ethereum_private_key
        new_account = accounts.add(private_key=private_key)

        txn_dict = {'from': new_account}

        receipt = luce_project.ConsentCode.at(
            self.contract_address).giveResearchPurpose(
                user.ethereum_public_key, rp.use_for_methods_development,
                rp.use_for_reference_or_control_material,
                rp.use_for_research_concerning_populations,
                rp.use_for_research_ancestry, rp.use_for_biomedical_research,
                txn_dict)

        # tx = web3.give_general_research_purpose(self, user, estimate)
        logger.info(receipt)
        return receipt.status


class DataContract(models.Model):
    contract_address = models.CharField(max_length=255, null=True, unique=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    commitment = models.CharField(max_length=255, null=False, default='0x0')

    consent_contract = models.ForeignKey(ConsentContract,
                                         on_delete=models.CASCADE,
                                         null=True)

    description = models.CharField(max_length=255, null=True)

    licence = models.IntegerField(default=1)

    link = models.CharField(max_length=255, null=True)

    def get_a_new_account(self):
        new_account = accounts.add()
        accounts[0].transfer(new_account, 1e18)
        return new_account

    def require_verifier_deployed(self):
        try:
            v = Verifier.objects.get(pk=1)

            if v.address is None:
                deploy_result = v.deploy()
                # print(deploy_result)

                v.address = deploy_result.address
                v.save()
        except ObjectDoesNotExist:
            v = Verifier.objects.create(pk=1)
            r = v.deploy()

            print(r)
            # v.address = v.deploy().address
            v.save()

    def deploy(self):

        # private_key = self.user.ethereum_private_key
        # new_account = accounts.add(private_key=private_key)
        new_account = self.get_a_new_account()
        # accounts[1].transfer(new_account, 1e18)  # 1 ether
        # print(new_account)

        self.require_verifier_deployed()
        verifier_address = Verifier.objects.get(pk=1).address
        # print(verifier_address)

        # commitment = self.get_commitment("hello")
        commitment = {"public_signals":['16279978653553831575017442062517458639822344791369834134794885970235221444339']}
        # commitment = "16279978653553831575017442062517458639822344791369834134794885970235221444339n"
        print(commitment)

        # print(accounts.at())
        contract = luce_project.LuceMain.deploy(verifier_address,
                                                commitment['public_signals'],
                                                {'from': new_account})

        self.contract_address = contract.address
        self.save()
        return contract.tx.txid

    def get_commitment(self, secret):
        http = urllib3.PoolManager()
        snark_service_url = "http://zkp_service:8888/compute_commitment"
        body_json = json.dumps({"secret": secret}).encode('utf-8')

        print(body_json)

        r = http.request('POST',
                         snark_service_url,
                         body=body_json,
                         headers={'Content-Type': 'application/json'})

        
        result = json.loads(r.data.decode('utf-8'))

        print(result)
        return result

    def deploy_contract(self):
        # self.deploy()

        tx_receipt = web3.deploy_contract_main(self.user)
        if type(tx_receipt) is list:
            return tx_receipt
        self.contract_address = tx_receipt["contractAddress"]
        self.save()
        return tx_receipt

    def set_registry_address(self, registry_address):
        new_account = self.get_a_new_account()
        transaction_dict = {'from': new_account}

        transaction_receipt = luce_project.LuceMain.at(
            self.contract_address).setRegistryAddress(registry_address,
                                                      transaction_dict)

        return transaction_receipt.status

    # def set_registry_address(self, registry, estimate):
    #     tx_receipt = web3.set_registry_address(self, registry.contract_address,
    #                                            estimate)
    #     return tx_receipt

    def set_consent_address(self):
        new_account = self.get_a_new_account()
        transaction_dict = {'from': new_account}

        transaction_receipt = luce_project.LuceMain.at(
            self.contract_address).setConsentAddress(
                self.consent_contract.contract_address, transaction_dict)

        return transaction_receipt.status

        # tx_receipt = web3.set_consent_address(
        #     self, self.consent_contract.contract_address, estimate)
        # return tx_receipt

    def publish_dataset(self, link):
        new_account = self.get_a_new_account()
        transaction_dict = {
            'from': new_account,
        }

        print(transaction_dict)

        transaction_receipt = luce_project.LuceMain.at(
            self.contract_address).publishData(self.description, link,
                                               self.licence, transaction_dict)

        return transaction_receipt.status
        # tx = web3.publish_dataset(self, user, link)
        # return tx

    def retreive_info(self):
        tx_receipt = web3.retreive_dataset_info(self)
        return tx_receipt

    def add_data_requester(self, access_time, purpose_code, user, estimate):
        acc = accounts.add(private_key=user.ethereum_private_key)

        txn_dict = {'from': acc, "gas_limit": 1e15, "allow_revert": True}

        tx_receipt = luce_project.LuceMain.at(
            self.contract_address).addDataRequester(purpose_code, access_time,
                                                    txn_dict)

        return tx_receipt

    def getLink(self, user, estimate):
        new_account = self.get_a_new_account()
        transaction_dict = {'from': new_account}


        
        receipt = luce_project.LuceMain.at(self.contract_address).getLink(transaction_dict)
        logger.info(receipt)
        return receipt
        

        # logger.info(receipt)

        # return 0


    def checkAccess(self, user, researchpurpose):
        hasAccess = web3.checkAccess(self, user, researchpurpose)
        return hasAccess


class LuceRegistry(models.Model):
    contract_address = models.CharField(max_length=255, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def deploy(self):

        # account[0] as the administrator
        result = luce_project.LUCERegistry.deploy({'from': accounts[0]})
        if result.tx.status == 1:
            self.contract_address = result.address
            print("Deploy LUCERegistry contract succeeded")
        else:
            print("Deploy LUCERegistry contract failed")

        return result.tx.status

    def deploy_contract(self):
        tx_receipt = web3.deploy_registry(self.user)
        if type(tx_receipt) is list:
            return tx_receipt
        self.contract_address = tx_receipt["contractAddress"]
        return tx_receipt

    def is_registered(self, user, usertype):
        if usertype == 'requester':
            return self.is_registered_as_requester(user)

    def is_registered_as_requester(self, user):
        result = luce_project.LUCERegistry.at(self.contract_address).checkUser(
            user.ethereum_public_key)
        return result

        # isregistered = web3.is_registered(self, user, usertype)
        # return isregistered

    def register_provider(self, user, estimate):
        tx = web3.register_provider(self, user, estimate)
        return tx

    def register_requester(self, user, license, estimate):
        logger.info(user.ethereum_private_key)
        logger.info(user.ethereum_public_key)

        sender = accounts.add(private_key=user.ethereum_private_key)
        result = luce_project.LUCERegistry.at(self.contract_address).registerNewUser(
            user.ethereum_public_key, 
            license, 
            {
                'from': sender
                }
            )
        print(result)
        # tx = web3.register_requester(self, user, license, estimate)
        return result



"""

class Cause(models.Model):

    title = models.CharField(max_length=255)
    goal = models.IntegerField(default=0)
    description = models.CharField(max_length=255, blank=True, null=True)
    ethereum_private_key = models.CharField(max_length=255, blank=True, null=True)
    ethereum_public_key = models.CharField(max_length=255, blank=True, null=True)
    percentBPS = models.IntegerField(validators=[MaxValueValidator(10000), MinValueValidator(0)], default=10000)
    creator = models.ForeignKey(User, null=True, on_delete=models.CASCADE)


class Donation(models.Model):
    cause = models.ForeignKey(Cause, on_delete=models.CASCADE)
    donor = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField(default = 0)



class CauseGroup(models.Model):
    name = models.CharField(max_length=255, default = '')
    description = models.CharField(max_length=255, default = '')
    creator = models.ForeignKey(User, null=True, on_delete=models.CASCADE)



    
class GroupInfo(models.Model):
    cause = models.ForeignKey(Cause, on_delete=models.CASCADE)
    group = models.ForeignKey(CauseGroup, related_name='group', on_delete=models.CASCADE, null = True)
    split = models.IntegerField(validators=[MaxValueValidator(10000), MinValueValidator(0)])
    
"""

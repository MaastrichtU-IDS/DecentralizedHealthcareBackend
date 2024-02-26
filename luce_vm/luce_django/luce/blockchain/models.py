from privacy.snarkjs_service import SnarkjsService
from django.db import models
from accounts.models import User
from brownie import network, project, accounts
from django.core.exceptions import ObjectDoesNotExist
from utils.utils import get_initial_response, set_logger
from .singleton import SingletonModel, SingletonContractModel
from privacy.disposable_address import DisposableAddressService

logger = set_logger(__file__)

# Tips:
# We can not import the following here, because the name just can be provided(resolved) after the app is loaded.
# So just import them in the functions where they are used.
# from brownie.project.BrownieProject import *


snarkjs_service = SnarkjsService()


class Restrictions(models.Model):
    no_restrictions = models.BooleanField()
    open_to_general_research_and_clinical_care = models.BooleanField()
    open_to_HMB_research = models.BooleanField()
    open_to_population_and_ancestry_research = models.BooleanField()
    open_to_disease_specific = models.BooleanField()


class PrimaryCategory(models.Model):
    no_restrictions = models.BooleanField(default=False)
    open_to_general_research_and_clinical_care = models.BooleanField(
        default=False)
    open_to_HMB_research = models.BooleanField(default=False)
    open_to_population_and_ancestry_research = models.BooleanField(
        default=False)
    open_to_disease_specific = models.BooleanField(default=False)


class SecondaryCategory(models.Model):
    open_to_genetic_studies_only = models.BooleanField()
    research_specific_restrictions = models.BooleanField()
    open_to_research_use_only = models.BooleanField()
    no_general_method_research = models.BooleanField()


class Requirements(models.Model):
    geographic_specific_restriction = models.BooleanField()
    open_to_non_profit_use_only = models.BooleanField()
    publication_required = models.BooleanField()
    collaboration_required = models.BooleanField()
    ethics_approval_required = models.BooleanField()
    time_limit_on_use = models.BooleanField()
    cost_on_use = models.BooleanField()
    data_security_measures_required = models.BooleanField()


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


class PlonkVerifierContract(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # if not self.address:
        #     self.deploy()
        super().save(*args, **kwargs)

    def deploy(self):
        from brownie import accounts
        from brownie.project.BrownieProject import PlonkVerifier

        # 1. deploy contract
        contract = PlonkVerifier.deploy({'from': accounts[0]})
        self.address = contract.address

        # 2. save contract address
        self.save()

        return contract.tx


class LuceRegistryContract(models.Model):
    contract_address = models.CharField(max_length=255, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def deploy(self):
        # from brownie import accounts
        from brownie.project.BrownieProject import LUCERegistry

        # account[0] as the administrator
        contract = LUCERegistry.deploy({'from': accounts[0]})
        receipt = contract.tx
        if receipt.status == 1:
            self.contract_address = receipt.contract_address
            print("Deploy LUCERegistry contract succeeded")
        else:
            print("Deploy LUCERegistry contract failed")

        return receipt.status

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
        from brownie.project.BrownieProject import LUCERegistry
        result = LUCERegistry.at(self.contract_address).checkUser(
            user.ethereum_public_key)
        return result

        # isregistered = web3.is_registered(self, user, usertype)
        # return isregistered

    def register_provider(self, user, estimate):
        tx = web3.register_provider(self, user, estimate)
        return tx

    def register_requester(self, user, license, estimate):
        from brownie.project.BrownieProject import LUCERegistry

        print("register_requester")
        print(license)

        sender = accounts.add(private_key=user.ethereum_private_key)
        result = LUCERegistry.at(self.contract_address).registerNewUser(
            user.ethereum_public_key, license, {'from': sender})
        return result


class ConsentContract(models.Model):
    contract_address = models.CharField(max_length=255, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restrictions = models.ForeignKey(Restrictions, on_delete=models.CASCADE)

    # primary_category = models.ForeignKey(PrimaryCategory,
    #                                      on_delete=models.CASCADE)
    # secondary_category = models.ForeignKey(SecondaryCategory,
    #                                        on_delete=models.CASCADE)
    # requirements = models.ForeignKey(Requirements, on_delete=models.CASCADE)

    research_purpose = models.ForeignKey(ResearchPurpose,
                                         on_delete=models.CASCADE,
                                         null=True)

    def get_a_new_account(self, amount=1e15):
        disposable_address_service = DisposableAddressService()
        user_account = accounts.add(self.user.ethereum_private_key)

        print("user_account: " + str(user_account))
        new_account = disposable_address_service.get_a_new_address_with_balance(
            sender=user_account, amount=amount)
        print("new_account: " + str(new_account))

        return new_account

    def update_data_consent(self):
        from brownie.project.BrownieProject import ConsentCode
        new_account = self.get_a_new_account(amount=1e17)

        print("new_account: " + str(new_account))
        print("balance: " + str(new_account.balance()))
        transaction_dict = {'from': new_account}

        consent_contract = ConsentCode.at(self.contract_address)

        print("consent_contract: " + str(consent_contract))
        transaction_receipt = ConsentCode.at(
            self.contract_address).UploadDataPrimaryCategory(
                self.user.ethereum_public_key,
                self.restrictions.no_restrictions,
                self.restrictions.open_to_general_research_and_clinical_care,
                self.restrictions.open_to_HMB_research,
                self.restrictions.open_to_population_and_ancestry_research,
                self.restrictions.open_to_disease_specific, transaction_dict)

        # ConsentCode.at(self.contract_address).UploadDataSecondaryCategory(
        #     self.user.ethereum_public_key,
        #     self.secondary_category.open_to_genetic_studies_only,
        #     self.secondary_category.research_specific_restrictions,
        #     self.secondary_category.open_to_research_use_only,
        #     self.secondary_category.no_general_method_research,
        #     transaction_dict)

        # ConsentCode.at(self.contract_address).UploadDataRequirements(
        #     self.user.ethereum_public_key,
        #     self.requirements.geographic_specific_restriction,
        #     self.requirements.open_to_non_profit_use_only,
        #     self.requirements.publication_required,
        #     self.requirements.collaboration_required,
        #     self.requirements.ethics_approval_required,
        #     self.requirements.time_limit_on_use, self.requirements.cost_on_use,
        #     self.requirements.data_security_measures_required,
        #     transaction_dict)

        return transaction_receipt.status

    def upload_data_consent(self, estimate):
        return web3.upload_data_consent(self, estimate)

    def retrieve_contract_owner(self):
        return web3.retrieve_contract_owner(self)

    def deploy(self):
        from brownie.project.BrownieProject import ConsentCode
        new_account = self.get_a_new_account(amount=1e17)

        logger.info("new_account: " + str(new_account))
        print("new_account: " + str(new_account))
        print("new_account: " + str(new_account))
        print("balance: " + str(new_account.balance()))
        contract = ConsentCode.deploy({'from': new_account})

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
        from brownie.project.BrownieProject import ConsentCode
        rp = self.research_purpose.clinical_purpose

        private_key = self.user.ethereum_private_key
        new_account = accounts.add(private_key=private_key)

        # new_account = self.get_a_new_account()

        txn_dict = {'from': new_account}

        receipt = ConsentCode.at(self.contract_address).giveClinicalPurpose(
            user.ethereum_public_key, rp.use_for_decision_support,
            rp.use_for_disease_support, txn_dict)

        # logger.info(receipt)

        return receipt.status

        # tx = web3.give_clinical_research_purpose(self, user, estimate)
        # return tx

    def give_HMB_research_purpose(self, user, estimate):
        from brownie.project.BrownieProject import ConsentCode
        rp = self.research_purpose.HMB_research_purpose
        private_key = self.user.ethereum_private_key
        new_account = accounts.add(private_key=private_key)
        # new_account = self.get_a_new_account()

        txn_dict = {'from': new_account}

        receipt = ConsentCode.at(self.contract_address).giveHMBPurpose(
            user.ethereum_public_key,
            rp.use_for_research_concerning_fundamental_biology,
            rp.use_for_research_concerning_genetics,
            rp.use_for_research_concerning_drug_development,
            rp.use_for_research_concerning_any_disease,
            rp.use_for_research_concerning_age_categories,
            rp.use_for_research_concerning_gender_categories, txn_dict)

        # logger.info(receipt)
        return receipt.status

    def give_general_research_purpose(self, user, estimate):
        from brownie.project.BrownieProject import ConsentCode
        rp = self.research_purpose.general_research_purpose
        private_key = self.user.ethereum_private_key
        new_account = accounts.add(private_key=private_key)
        # new_account = self.get_a_new_account()

        txn_dict = {'from': new_account}

        receipt = ConsentCode.at(self.contract_address).giveResearchPurpose(
            user.ethereum_public_key, rp.use_for_methods_development,
            rp.use_for_reference_or_control_material,
            rp.use_for_research_concerning_populations,
            rp.use_for_research_ancestry, rp.use_for_biomedical_research,
            txn_dict)

        # tx = web3.give_general_research_purpose(self, user, estimate)
        # logger.info(receipt)
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
        disposable_address_service = DisposableAddressService()
        user_account = accounts.add(self.user.ethereum_private_key)
        new_account = disposable_address_service.get_a_new_address_with_balance(
            sender=user_account, amount=1e17)

        # new_account = accounts.add()
        # accounts[0].transfer(new_account, 1e18)
        return new_account

    def require_verifier_deployed(self):
        try:
            v = PlonkVerifierContract.objects.get(pk=1)

            if v.address is None:
                deploy_result = v.deploy()
                # print(deploy_result)

                v.address = deploy_result.address
                v.save()
        except ObjectDoesNotExist:
            v = PlonkVerifierContract.objects.create(pk=1)
            r = v.deploy()

            print(r)
            # v.address = v.deploy().address
            # v.save()

    def deploy(self):
        from brownie.project.BrownieProject import LuceMain

        # private_key = self.user.ethereum_private_key
        # new_account = accounts.add(private_key=private_key)
        new_account = self.get_a_new_account()
        # accounts[1].transfer(new_account, 1e18)  # 1 ether
        # print(new_account)

        self.require_verifier_deployed()
        verifier_address = PlonkVerifierContract.objects.get(pk=1).address
        # print(verifier_address)
        logger.info("verifier_address: ")
        logger.info(verifier_address)

        # commitment = self.get_commitment("hello")
        proof = snarkjs_service.generate_proof("hello")

        logger.info("proof")
        logger.info(str(proof['public_signals']))

        commitment = {
            "public_signals": proof['public_signals']

        }

        contract = LuceMain.deploy({'from': new_account})

        logger.info("contract")
        logger.info(contract)

        self.contract_address = contract.address
        self.save()
        return contract.tx.status

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
        from brownie.project.BrownieProject import LuceMain
        # self.deploy()

        tx_receipt = web3.deploy_contract_main(self.user)
        if type(tx_receipt) is list:
            return tx_receipt
        self.contract_address = tx_receipt["contractAddress"]
        self.save()
        return tx_receipt

    def set_registry_address(self, registry_address):
        from brownie.project.BrownieProject import LuceMain
        new_account = self.get_a_new_account()
        transaction_dict = {'from': new_account}

        transaction_receipt = LuceMain.at(
            self.contract_address).setRegistryAddress(registry_address,
                                                      transaction_dict)

        return transaction_receipt.status

    # def set_registry_address(self, registry, estimate):
    #     tx_receipt = web3.set_registry_address(self, registry.contract_address,
    #                                            estimate)
    #     return tx_receipt

    def set_consent_address(self):
        from brownie.project.BrownieProject import LuceMain
        new_account = self.get_a_new_account()
        transaction_dict = {'from': new_account}

        transaction_receipt = LuceMain.at(
            self.contract_address).setConsentAddress(
                self.consent_contract.contract_address, transaction_dict)

        return transaction_receipt.status

        # tx_receipt = web3.set_consent_address(
        #     self, self.consent_contract.contract_address, estimate)
        # return tx_receipt

    def publish_dataset(self, link):
        from brownie.project.BrownieProject import LuceMain
        new_account = self.get_a_new_account()
        transaction_dict = {
            'from': new_account,
        }

        print("Dataset license: " + str(self.licence))

        transaction_receipt = LuceMain.at(self.contract_address).publishData(
            self.description, link, self.licence, transaction_dict)

        return transaction_receipt.status
        # tx = web3.publish_dataset(self, user, link)
        # return tx

    def retreive_info(self):
        tx_receipt = web3.retreive_dataset_info(self)
        return tx_receipt

    def add_data_requester(self, access_time, purpose_code, user, estimate):
        from brownie.project.BrownieProject import LuceMain
        sender = user_account = accounts.at(user.ethereum_public_key)
        # disposable_address_service = DisposableAddressService()
        # acc = disposable_address_service.get_a_new_address_with_balance(
        #     sender=sender, amount=1e15)

        txn_dict = {'from': sender}

        tx_receipt = LuceMain.at(self.contract_address).addDataRequester(
            purpose_code, access_time, txn_dict)

        return tx_receipt.status

    def getLink(self, user, estimate):
        from brownie.project.BrownieProject import LuceMain
        new_account = self.get_a_new_account()
        transaction_dict = {'from': new_account}

        receipt = LuceMain.at(self.contract_address).getLink(transaction_dict)
        logger.info(receipt)
        return receipt

        # logger.info(receipt)

        # return 0

    # def checkAccess(self, user, researchpurpose):
    #     hasAccess = web3.checkAccess(self, user, researchpurpose)
    #     return hasAccess

    def checkAccess(self, user, researchpurpose):
        from brownie.project.BrownieProject import LuceMain, ConsentCode
        new_account = self.get_a_new_account()
        transaction_dict = {'from': new_account}

        # 1. get restrictions from dataset
        restrictions = self.consent_contract.restrictions

        # 2. get all restrictions and purposes
        all_restrictions_and_purposes = self.getAllRestrictionsAndPurposes(
            restrictions, researchpurpose)

        consent_contract_address = self.consent_contract.contract_address
        consent_contract = ConsentCode.at(consent_contract_address)

        access_granted = consent_contract.CheckAccess(
            all_restrictions_and_purposes, transaction_dict
        )

        return access_granted

    def getAllRestrictionsAndPurposes(self, restrictions, researchpurpose):
        final = [False for x in range(0, 49)]

        restrictions_ids = {
            0: "no_restrictions",
            1: "open_to_general_research_and_clinical_care",
            16: "open_to_population_and_ancestry_research",
            19: "open_to_disease_specific",
            8: "open_to_HMB_research"
        }
        generalResearchPurpose_ids = {
            2: "use_for_methods_development",
            3: "use_for_reference_or_control_material",
            17: "use_for_research_concerning_populations",
            18: "use_for_research_ancestry",
            4: "use_for_biomedical_research"
        }
        hmbPurpose_ids = {
            9: "use_for_research_concerning_fundamental_biology",
            10: "use_for_research_concerning_genetics",
            11: "use_for_research_concerning_drug_development",
            12: "use_for_research_concerning_any_disease",
            13: "use_for_research_concerning_age_categories",
            14: "use_for_research_concerning_gender_categories"
        }

        for id in restrictions_ids.keys():
            final[id] = getattr(restrictions, restrictions_ids[id]) if hasattr(
                restrictions, restrictions_ids[id]) else False

        for id in generalResearchPurpose_ids.keys():
            final[id] = getattr(researchpurpose.general_research_purpose,
                                generalResearchPurpose_ids[id]) if hasattr(
                                    researchpurpose.general_research_purpose,
                                    generalResearchPurpose_ids[id]) else False

        for id in hmbPurpose_ids.keys():
            final[id] = getattr(researchpurpose.HMB_research_purpose,
                                hmbPurpose_ids[id]) if hasattr(
                                    researchpurpose.HMB_research_purpose,
                                    hmbPurpose_ids[id]) else False
        # for x in range(0,49):
        # print(str(final[x])+" ["+str(x)+"]")
        return final

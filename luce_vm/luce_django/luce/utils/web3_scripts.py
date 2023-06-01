# from web3.middleware import geth_poa_middleware
import os
from web3 import Web3
import time

ganache = False

###CONNECT TO ETH NETWORK USING HOSTED NODE (infura)##########
#w3 = Web3(Web3.HTTPProvider("https://rinkeby.infura.io/v3/374de38210c343f1921a77b45822edf9"))
#CHAIN_ID = 4

###CONNECT TO ETH NETWORK USING LOCAL LIGHT NODE (GETH)##########
#w3 = Web3(Web3.IPCProvider("/home/vagrant/.ethereum/rinkeby/geth.ipc"))
#CHAIN_ID = 4

###CONNECT TO POLYGON NETWORK USING HOSTED NODE##########
# w3 = Web3(Web3.HTTPProvider("https://rpc-mumbai.matic.today"))
# CHAIN_ID = 80001

###CONNECT TO GANACHE LOCAL NETWORK##########
GANACHE_ADDRESS = 'http://ganache_db'
GANACHE_PORT = os.getenv('GANACHE_PORT')
GANACHE_PORT = "8545"
GANACHE_URI = GANACHE_ADDRESS + ':' + GANACHE_PORT

BLOCKCHAIN_URI = GANACHE_URI

w3 = Web3(Web3.HTTPProvider(BLOCKCHAIN_URI))
CHAIN_ID = 1337
ganache = True

# w3.middleware_stack.inject(geth_poa_middleware, layer=0)

BASE_DIR = os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))) + "/utils/data/"
# '/vagrant/luce_django/luce'
MAIN_CONTRACT_PATH = BASE_DIR + 'Main.sol'
CONSENT_CONTRACT_PATH = BASE_DIR + 'ConsentCode.sol'
REGISTRY_CONTRACT_PATH = BASE_DIR + 'LuceRegistry.sol'

CONTRACT_FILE = "LUCERegistry"
LUCEMAIN_CONTRACT = "LuceMain"
CONSENT_CONTRACT = "ConsentCode"

DEBUG = True

# WEB3 HELPER FUNCTIONS ####g
# Helper functions used to make the code in assign_address_v3 easier to read

# Create faucet for pre-funding accounts
# NOTE: placing a private key here is obviously very unsafe
# We only do this for development usage. When transitioning
# to Infura the faucet can be replaced with an API call instead.

# Private key (obtained via Ganache interface)
faucet_privateKey = "56c6de6fd54438dbb31530f5fdeeaada0b1517880c91dfcd46a4e5fec59a9c79"
# faucet_privateKey = "0x5714ad5f65fb27cb0d0ab914db9252dfe24cf33038a181555a7efc3dcf863ab3"

if ganache:
    faucet_privateKey = "56c6de6fd54438dbb31530f5fdeeaada0b1517880c91dfcd46a4e5fec59a9c79"
# Establish faucet account
faucet = w3.eth.account.privateKeyToAccount(faucet_privateKey)


def create_wallet():
    eth_account = w3.eth.account.create()
    return (eth_account)


def send_ether(amount_in_ether, recipient_address, sender_pkey):
    amount_in_wei = w3.toWei(amount_in_ether, 'ether')
    # Obtain sender address from private key
    sender_address = w3.eth.account.privateKeyToAccount(sender_pkey).address
    # How many transactions have been made by wallet?
    # This is required and prevents double-spending.
    # Same name but different from nonce in block mining.
    nonce = w3.eth.getTransactionCount(sender_address)
    # Specify transcation dictionary
    txn_dict = {
        'from': sender_address,
        'to': recipient_address,
        'value': amount_in_wei,
        'gasPrice': w3.toWei('10', 'Gwei'),
        'nonce': nonce,
        'chainId': CHAIN_ID
    }

    # IN THIS STEP THE PRIVATE KEY OF THE SENDER IS USED
    # Sign transaction

    gas = transact_function(w3.eth.estimateGas, txn_dict,
                            "estimating gas for sending ether")
    if type(gas) is list:
        return gas

    txn_dict["gas"] = gas

    # print(txn_dict)

    txn_receipt = sign_and_send(txn_dict, sender_pkey,
                                "sending ether from faucet to account")
    return txn_receipt


#### ASSIGN ADDRESS ####
# This script takes a Django user object as input and
# creates a fresh ethereum account for the user.
# It will also pre-fund the new account with some ether.


def assign_address_v3():
    # Establish web3 connection
    import time
    from hexbytes import HexBytes
    # Create new web3 account
    eth_account = create_wallet()
    txn_receipt = send_ether(amount_in_ether=1.5,
                             recipient_address=eth_account.address,
                             sender_pkey=faucet.privateKey)
    # Return user, now with wallet associated
    return txn_receipt, eth_account


def check_balance(user):
    balance_contract = w3.eth.getBalance(user.contract_address)
    balance_user = w3.eth.getBalance(user.ethereum_public_key)
    final = {
        "contract balance": balance_contract,
        "address balance": balance_user
    }
    return final


def deploy_registry(_user):
    return deploy(_user, REGISTRY_CONTRACT_PATH, CONTRACT_FILE)


def deploy_contract_main(_user):
    return deploy(_user, MAIN_CONTRACT_PATH, LUCEMAIN_CONTRACT)


def deploy_consent(_user):
    return deploy(_user, CONSENT_CONTRACT_PATH, CONSENT_CONTRACT)


def deploy(_user, contract, interface):
    from web3 import Web3
    contract_interface = compile_and_extract_interface(contract, interface)

    # Extract abi and bytecode
    abi = contract_interface['abi']
    bytecode = contract_interface['bin']
    contract = w3.eth.contract(abi=abi, bytecode=bytecode)

    # Obtain contract address & instantiate contract
    user_address = _user.ethereum_public_key
    private_key = _user.ethereum_private_key
    nonce = w3.eth.getTransactionCount(user_address)

    txn_dict = {
        'from': user_address,
        'chainId': CHAIN_ID,
        'gasPrice': w3.toWei('20', 'gwei'),
        'nonce': nonce,
    }

    gas = transact_function(
        contract.constructor().estimateGas, {},
        "estimating gas for: " + interface + " constructor") * 2

    if type(gas) is list:
        return gas
    txn_dict["gas"] = gas

    gas = transact_function(contract.constructor().buildTransaction, txn_dict,
                            "building transactino: deployment of " + interface)
    if type(gas) is list:
        return gas
    contract_txn = contract.constructor().buildTransaction(txn_dict)

    return sign_and_send(contract_txn, private_key,
                         "sending transaction: deployment of " + interface)


def compile_and_extract_interface_Consent():
    return compile_and_extract_interface(CONSENT_CONTRACT_PATH,
                                         CONSENT_CONTRACT)


def compile_and_extract_interface_Registry():
    return compile_and_extract_interface(REGISTRY_CONTRACT_PATH, CONTRACT_FILE)


def compile_and_extract_interface_Main():
    return compile_and_extract_interface(MAIN_CONTRACT_PATH, LUCEMAIN_CONTRACT)


def compile_and_extract_interface(contract, interface):
    import solcx
    from solcx import compile_source

    # Read in LUCE contract code
    with open(contract,
              'r') as file:  # Adjust file_path for use in Jupyter/Django
        contract_source_code = file.read()

    # Compile & Store Compiled source code

    compiled_sol = compile_source(contract_source_code, solc_version="0.6.2")

    # Extract full interface as dict from compiled contract
    contract_interface = compiled_sol['<stdin>:' + interface]

    # Extract abi and bytecode
    abi = contract_interface['abi']
    bytecode = contract_interface['bin']

    # Create dictionary with interface
    d = dict()
    d['abi'] = abi
    d['bin'] = bytecode
    d['full_interface'] = contract_interface
    return (d)


def upload_data_consent(consent_obj, estimate):
    from web3 import Web3
    restrictions = consent_obj.restrictions
    user = consent_obj.user
    contract_address = consent_obj.contract_address

    noRestrictions = restrictions.no_restrictions
    openToGeneralResearchAndClinicalCare = restrictions.open_to_general_research_and_clinical_care
    openToHMBResearch = restrictions.open_to_HMB_research
    openToPopulationAndAncestryResearch = restrictions.open_to_population_and_ancestry_research
    openToDiseaseSpecific = restrictions.open_to_disease_specific

    d = compile_and_extract_interface_Consent()
    abi = d["abi"]

    user_address = user.ethereum_public_key
    private_key = user.ethereum_private_key

    # Here, we get a `ConsnetCode` contract
    contract_instance = w3.eth.contract(address=contract_address, abi=abi)
    user = w3.eth.account.privateKeyToAccount(private_key)

    nonce = w3.eth.getTransactionCount(user_address)
    txn_dict = {
        'from': user_address,
        'chainId': CHAIN_ID,
        'gasPrice': w3.toWei('20', 'gwei'),
        'nonce': nonce,
    }
    gas = transact_function(
        contract_instance.functions.UploadDataPrimaryCategory(
            user_address, noRestrictions, openToGeneralResearchAndClinicalCare,
            openToHMBResearch, openToPopulationAndAncestryResearch,
            openToDiseaseSpecific).estimateGas, txn_dict,
        "estimating gas for: upload consent statements to ConsentContract")

    if type(gas) is list:
        return gas
    if estimate:
        return gas

    txn_dict['gas'] = gas

    contract_txn = transact_function(
        contract_instance.functions.UploadDataPrimaryCategory(
            user_address, noRestrictions, openToGeneralResearchAndClinicalCare,
            openToHMBResearch, openToPopulationAndAncestryResearch,
            openToDiseaseSpecific).buildTransaction, txn_dict,
        "building transaction: upload consent statements to ConsentContract")
    if type(contract_txn) is list:
        return gas
    return sign_and_send(
        contract_txn, private_key,
        "sending transactin: upload consent statements to ConsentContract")


def give_clinical_research_purpose(consentContract, user, estimate):
    from web3 import Web3
    contract_address = consentContract.contract_address
    rp = consentContract.research_purpose.clinical_purpose

    d = compile_and_extract_interface_Consent()
    abi = d["abi"]
    user_address = user.ethereum_public_key
    private_key = user.ethereum_private_key
    contract_instance = w3.eth.contract(address=contract_address, abi=abi)
    user = w3.eth.account.privateKeyToAccount(private_key)
    nonce = w3.eth.getTransactionCount(user_address)
    txn_dict = {
        'from': user_address,
        'chainId': CHAIN_ID,
        'gasPrice': w3.toWei('20', 'gwei'),
        'nonce': nonce,
    }
    gas = transact_function(
        contract_instance.functions.giveClinicalPurpose(
            user_address, rp.use_for_decision_support,
            rp.use_for_disease_support).estimateGas, {},
        "estimating gas for setting clinical purpose in the consent contract")
    if type(gas) is list:
        return gas
    txn_dict["gas"] = gas
    if estimate:
        return gas
    contract_txn = transact_function(
        contract_instance.functions.giveClinicalPurpose(
            user_address, rp.use_for_decision_support,
            rp.use_for_disease_support).buildTransaction, txn_dict,
        "building transaction: setting clinical purpose in the consent contract"
    )
    if type(contract_txn) is list:
        return contract_txn
    return sign_and_send(
        contract_txn, private_key,
        "sending transaction: setting clinical purpose in the consent contract"
    )


def give_HMB_research_purpose(consentContract, user, estimate):
    from web3 import Web3
    contract_address = consentContract.contract_address
    rp = consentContract.research_purpose.HMB_research_purpose

    d = compile_and_extract_interface_Consent()
    abi = d["abi"]
    user_address = user.ethereum_public_key
    private_key = user.ethereum_private_key
    contract_instance = w3.eth.contract(address=contract_address, abi=abi)
    user = w3.eth.account.privateKeyToAccount(private_key)
    nonce = w3.eth.getTransactionCount(user_address)
    txn_dict = {
        'from': user_address,
        'chainId': CHAIN_ID,
        'gasPrice': w3.toWei('20', 'gwei'),
        'nonce': nonce,
    }
    gas = transact_function(
        contract_instance.functions.giveHMBPurpose(
            user_address, rp.use_for_research_concerning_fundamental_biology,
            rp.use_for_research_concerning_genetics,
            rp.use_for_research_concerning_drug_development,
            rp.use_for_research_concerning_any_disease,
            rp.use_for_research_concerning_age_categories,
            rp.use_for_research_concerning_gender_categories).estimateGas, {},
        "estimating gas for setting HMB ch purpose in the consent contract")
    if type(gas) is list:
        return gas
    txn_dict["gas"] = gas
    if estimate:
        return gas
    contract_txn = transact_function(
        contract_instance.functions.giveHMBPurpose(
            user_address, rp.use_for_research_concerning_fundamental_biology,
            rp.use_for_research_concerning_genetics,
            rp.use_for_research_concerning_drug_development,
            rp.use_for_research_concerning_any_disease,
            rp.use_for_research_concerning_age_categories,
            rp.use_for_research_concerning_gender_categories).buildTransaction,
        txn_dict,
        "building transaction: setting HMB research purpose in the consent contract"
    )
    if type(contract_txn) is list:
        return contract_txn
    return sign_and_send(
        contract_txn, private_key,
        "sending transaction: setting HMB research purpose in the consent contract"
    )


def give_general_research_purpose(consentContract, user, estimate):
    from web3 import Web3
    contract_address = consentContract.contract_address
    rp = consentContract.research_purpose.general_research_purpose

    d = compile_and_extract_interface_Consent()
    abi = d["abi"]
    user_address = user.ethereum_public_key
    private_key = user.ethereum_private_key
    contract_instance = w3.eth.contract(address=contract_address, abi=abi)
    user = w3.eth.account.privateKeyToAccount(private_key)
    nonce = w3.eth.getTransactionCount(user_address)
    txn_dict = {
        'from': user_address,
        'chainId': CHAIN_ID,
        'gasPrice': w3.toWei('20', 'gwei'),
        'nonce': nonce,
    }
    gas = transact_function(
        contract_instance.functions.giveResearchPurpose(
            user_address, rp.use_for_methods_development,
            rp.use_for_reference_or_control_material,
            rp.use_for_research_concerning_populations,
            rp.use_for_research_ancestry,
            rp.use_for_biomedical_research).estimateGas, {},
        "estimating gas for setting general research purpose in the consent contract"
    )
    if type(gas) is list:
        return gas
    txn_dict["gas"] = gas
    if estimate:
        return gas
    contract_txn = transact_function(
        contract_instance.functions.giveResearchPurpose(
            user_address, rp.use_for_methods_development,
            rp.use_for_reference_or_control_material,
            rp.use_for_research_concerning_populations,
            rp.use_for_research_ancestry,
            rp.use_for_biomedical_research).buildTransaction, txn_dict,
        "building transaction: setting general research purpose in the consent contract"
    )
    if type(contract_txn) is list:
        return contract_txn
    return sign_and_send(
        contract_txn, private_key,
        "sending transaction: setting general research purpose in the consent contract"
    )


def set_registry_address(datacontract, registry_address, estimate):
    from web3 import Web3
    d = compile_and_extract_interface_Main()
    abi = d["abi"]
    contract_address = datacontract.contract_address

    user = datacontract.user
    user_address = user.ethereum_public_key
    private_key = user.ethereum_private_key
    contract_instance = w3.eth.contract(address=contract_address, abi=abi)
    user = w3.eth.account.privateKeyToAccount(private_key)
    nonce = w3.eth.getTransactionCount(user_address)
    txn_dict = {
        'from': user_address,
        'chainId': CHAIN_ID,
        'gasPrice': w3.toWei('20', 'gwei'),
        'nonce': nonce,
    }

    gas = transact_function(
        contract_instance.functions.setRegistryAddress(
            registry_address).estimateGas, txn_dict,
        "estimating gas for setting registry address in Dataset contract")
    if type(gas) is list:
        return gas

    txn_dict["gas"] = gas
    if estimate:
        return gas

    contract_txn = transact_function(
        contract_instance.functions.setRegistryAddress(
            registry_address).buildTransaction, txn_dict,
        "building transaction: setting registry address in Dataset contract")
    return sign_and_send(
        contract_txn, private_key,
        "sending transaction: setting registry address in Dataset contract")


def is_registered(luceregistry, user, usertype):
    from web3 import Web3
    d = compile_and_extract_interface_Registry()
    abi = d["abi"]
    contract_address = luceregistry.contract_address
    user_address = user.ethereum_public_key
    private_key = user.ethereum_private_key
    contract_instance = w3.eth.contract(address=contract_address, abi=abi)
    user = w3.eth.account.privateKeyToAccount(private_key)
    nonce = w3.eth.getTransactionCount(user_address)
    txn_dict = {
        'from': user_address,
        'chainId': CHAIN_ID,
        'gasPrice': w3.toWei('20', 'gwei'),
        'nonce': nonce,
    }
    if usertype == "requester":
        isRegistered = contract_instance.functions.checkUser(
            user_address).call()  # returns a int (user exist if int != 0)
    else:
        isRegistered = contract_instance.functions.checkProvider(
            user_address).call()  # returns a boolean

    return isRegistered


def set_consent_address(datacontract, consent_address, estimate):
    from web3 import Web3
    d = compile_and_extract_interface_Main()
    abi = d["abi"]
    contract_address = datacontract.contract_address

    user = datacontract.user
    user_address = user.ethereum_public_key
    private_key = user.ethereum_private_key
    contract_instance = w3.eth.contract(address=contract_address, abi=abi)
    user = w3.eth.account.privateKeyToAccount(private_key)
    nonce = w3.eth.getTransactionCount(user_address)
    txn_dict = {
        'from': user_address,
        'chainId': CHAIN_ID,
        'gasPrice': w3.toWei('20', 'gwei'),
        'nonce': nonce,
    }

    gas = transact_function(
        contract_instance.functions.setConsentAddress(
            consent_address).estimateGas, txn_dict,
        "estimating gas for: setting consent address in Dataset contract")
    if type(gas) is list:
        return gas
    txn_dict["gas"] = gas
    if estimate:
        return gas

    contract_txn = transact_function(
        contract_instance.functions.setConsentAddress(
            consent_address).buildTransaction, txn_dict,
        "building transaction: setting consent address in Dataset contract")
    if type(contract_txn) is list:
        return contract_txn
    return sign_and_send(
        contract_txn, private_key,
        "sending transaction: setting consent address in Dataset contract")


def register_provider(registry, user, estimate):
    d = compile_and_extract_interface_Registry()
    abi = d["abi"]
    contract_address = registry.contract_address
    user = user
    user_address = user.ethereum_public_key
    private_key = user.ethereum_private_key
    contract_instance = w3.eth.contract(address=contract_address, abi=abi)
    user = w3.eth.account.privateKeyToAccount(private_key)
    nonce = w3.eth.getTransactionCount(user_address)

    txn_dict = {
        'from': user_address,
        'chainId': CHAIN_ID,
        'gasPrice': w3.toWei('20', 'gwei'),
        'nonce': nonce,
    }

    gas = transact_function(
        contract_instance.functions.newDataProvider(user_address).estimateGas,
        txn_dict,
        "estimating gas for: registering dataprovider in the LuceRegistry contract"
    )
    if type(gas) is list:
        return gas
    txn_dict["gas"] = gas

    if estimate:
        return gas

    contract_txn = transact_function(
        contract_instance.functions.newDataProvider(
            user_address).buildTransaction, txn_dict,
        "building transaction: registering dataprovider in the LuceRegistry contract"
    )
    if type(contract_txn) is list:
        return contract_txn
    return sign_and_send(
        contract_txn, private_key,
        "registering dataprovider in the LuceRegistry contract")


def register_requester(registry, user, license, estimate):
    d = compile_and_extract_interface_Registry()
    abi = d["abi"]
    contract_address = registry.contract_address
    user = user
    user_address = user.ethereum_public_key
    private_key = user.ethereum_private_key
    contract_instance = w3.eth.contract(address=contract_address, abi=abi)
    user = w3.eth.account.privateKeyToAccount(private_key)
    nonce = w3.eth.getTransactionCount(user_address)

    txn_dict = {
        'from': user_address,
        'chainId': CHAIN_ID,
        'gasPrice': w3.toWei('20', 'gwei'),
        'nonce': nonce,
    }

    gas = transact_function(
        contract_instance.functions.registerNewUser(user_address,
                                                    license).estimateGas, {},
        "estimating gas for: registering data requester in LuceRegistry contract"
    )
    if type(gas) is list:
        return gas
    txn_dict["gas"] = gas

    if estimate:
        return gas

    contract_txn = transact_function(
        contract_instance.functions.registerNewUser(user_address,
                                                    license).buildTransaction,
        txn_dict,
        "building transaction: registering data requester in LuceRegistry contract"
    )
    if type(contract_txn) is list:
        return contract_txn
    return sign_and_send(
        contract_txn, private_key,
        "registering data requester in LuceRegistry contract")


def publish_dataset(datacontract, user, link, estimate):

    description = datacontract.description
    licence = datacontract.licence
    d = compile_and_extract_interface_Main()
    abi = d["abi"]
    contract_address = datacontract.contract_address
    user = user
    user_address = user.ethereum_public_key
    private_key = user.ethereum_private_key
    contract_instance = w3.eth.contract(address=contract_address, abi=abi)
    user = w3.eth.account.privateKeyToAccount(private_key)
    nonce = w3.eth.getTransactionCount(user_address)

    txn_dict = {
        'from': user_address,
        'chainId': CHAIN_ID,
        'gasPrice': w3.toWei('20', 'gwei'),
        'nonce': nonce,
    }

    # gas = 650432#contract_instance.functions.publishData(description, link, licence).estimateGas(txn_dict)
    gas = transact_function(
        contract_instance.functions.publishData(description, link,
                                                licence).estimateGas, txn_dict,
        "estimating gas for: publishData function in Dataset Contract")
    if type(gas) is list:
        return gas

    txn_dict["gas"] = gas

    if estimate:
        return gas
    contract_txn = transact_function(
        contract_instance.functions.publishData(description, link,
                                                licence).buildTransaction,
        txn_dict,
        "building transaction: publishData function in Dataset Contract")
    if type(contract_txn) is list:
        return contract_txn
    return sign_and_send(
        contract_txn, private_key,
        "sending transaction: publishData function in Dataset Contract")


def get_link(datacontract, user, estimate):
    d = compile_and_extract_interface_Main()
    abi = d["abi"]
    contract_address = datacontract.contract_address

    user_address = user.ethereum_public_key
    private_key = user.ethereum_private_key
    contract_instance = w3.eth.contract(address=contract_address, abi=abi)
    user = w3.eth.account.privateKeyToAccount(private_key)
    nonce = w3.eth.getTransactionCount(user_address)

    txn_dict = {
        'from': user_address,
        'chainId': CHAIN_ID,
        'nonce': nonce,
    }

    try:
        contract_txn = contract_instance.functions.getLink().call(txn_dict)
    except ValueError as e:
        contract_txn = [e]
        print(e)
    return contract_txn


def add_data_requester(datacontract, access_time, purpose_code, user,
                       estimate):
    d = compile_and_extract_interface_Main()
    abi = d["abi"]
    contract_address = datacontract.contract_address
    user_address = user.ethereum_public_key
    private_key = user.ethereum_private_key
    contract_instance = w3.eth.contract(address=contract_address, abi=abi)
    user = w3.eth.account.privateKeyToAccount(private_key)
    nonce = w3.eth.getTransactionCount(user_address)

    txn_dict = {
        'from': user_address,
        'chainId': CHAIN_ID,
        'gasPrice': w3.toWei('20', 'gwei'),
        'nonce': nonce,
    }

    cost = contract_instance.functions.expectedCosts().call()
    txn_dict['value'] = cost

    gas = transact_function(
        contract_instance.functions.addDataRequester(1,
                                                     access_time).estimateGas,
        txn_dict,
        "estimating gas for: add data requester to the LuceMain contract")
    if type(gas) is list:
        return gas
    txn_dict["gas"] = gas

    if estimate:
        return gas

    contract_txn = contract_instance.functions.addDataRequester(
        1, access_time).buildTransaction(txn_dict)
    contract_txn = transact_function(
        contract_instance.functions.addDataRequester(
            1, access_time).buildTransaction, txn_dict,
        "building transaction: add data requester to the LuceMain contract")
    if type(contract_txn) is list:
        return contract_txn
    tx = sign_and_send(
        contract_txn, private_key,
        "sending transaction: add data requester to the LuceMain contract")
    return tx


def checkAccess(datacontract, user, researchpurpose):
    d = compile_and_extract_interface_Consent()
    abi = d["abi"]
    contract_address = datacontract.consent_contract.contract_address
    contract_instance = w3.eth.contract(address=contract_address, abi=abi)

    restrictions = datacontract.consent_contract.restrictions
    all_restrictions_and_purposes = getAllRestrictionsAndPurposes(
        restrictions, researchpurpose)

    hasAccess = contract_instance.functions.CheckAccess(
        all_restrictions_and_purposes).call()
    print(hasAccess)
    return hasAccess


def getAllRestrictionsAndPurposes(restrictions, researchpurpose):
    final = [False for x in range(0, 49)]
    print(researchpurpose)
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
    #print(str(final[x])+" ["+str(x)+"]")
    return final


def receipt_to_dict(tx_receipt, name):
    receipt = {}
    receipt["blockHash"] = tx_receipt.blockHash.hex()
    receipt["blockNumber"] = tx_receipt.blockNumber
    receipt["contractAddress"] = tx_receipt.contractAddress
    receipt["cumulativeGasUsed"] = tx_receipt.cumulativeGasUsed
    receipt["from"] = tx_receipt["from"]
    receipt["gasUsed"] = tx_receipt.gasUsed
    #receipt["logs"] = tx_receipt.logs
    receipt["logsBloom"] = tx_receipt.logsBloom.hex()
    receipt["status"] = tx_receipt.status
    receipt["to"] = tx_receipt.to
    receipt["transactionHash"] = tx_receipt.transactionHash.hex()
    receipt["transactionIndex"] = tx_receipt.transactionIndex
    receipt["transaction name"] = name

    return receipt


def sign_and_send(contract_txn, private_key, name):
    try:
        signed_txn = w3.eth.account.signTransaction(contract_txn, private_key)
        tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        transaction = receipt_to_dict(tx_receipt, name)
    except ValueError as e:
        if DEBUG:
            print()
            print(e)
        return [e, name]
    if DEBUG:
        pass
        # print("======================================================")
        # print(transaction)
    return transaction


def transact_function(func, dictionary, name):
    try:
        return func(dictionary)
    except ValueError as e:
        return [e, name]


"""
OLD CODE I KEEP FOR REFERENCES 


# Not used in Django Frontend anymore - kept for testing and reference
def create_wallet_old():
    print("This message comes from within my custom script")
    
    class EthAccount():
        address = None
        pkey = None

    def create_wallet():
        eth_account = EthAccount()
        eth_account_raw = w3.eth.account.create()
        eth_account.address = eth_account_raw.address
        eth_account.pkey = eth_account_raw.privateKey
        return (eth_account)

    eth_account = create_wallet()

    # Extract default accounts created by ganache
    accounts = w3.eth.accounts

    # Instantiate faucet object
    faucet = EthAccount()

    

    def send_ether(amount_in_ether, recipient_address, sender_address = faucet.address, sender_pkey=faucet.pkey):
        amount_in_wei = w3.toWei(amount_in_ether,'ether')

        # How many transactions have been made by wallet?
        # This is required and prevents double-spending.
        # Different from nonce in block mining.
        nonce = w3.eth.getTransactionCount(sender_address)
        
        # Specify transcation dictionary
        txn_dict = {
                'to': recipient_address,
                'value': amount_in_wei,
                'gas': 2000000,
                'gasPrice': w3.toWei('1', 'wei'),
                'nonce': nonce,
                'chainId': CHAIN_ID
        }
        
        # Sign transaction
        signed_txn = w3.eth.account.signTransaction(txn_dict, sender_pkey)

        # Send transaction & store transaction hash
        txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)

        # Check if transaction was added to blockchain
        # time.sleep(0.5)
        txn_receipt = w3.eth.getTransactionReceipt(txn_hash)
        return txn_hash

    # Send ether and store transaction hash
    txn_hash = send_ether(1.5,eth_account.address)

    # Show balance
    print("The balance of the new account is:\n")
    print(w3.eth.getBalance(eth_account.address))

    import os
 
    dirpath = os.getcwd()
    print("current directory is : " + dirpath)
    foldername = os.path.basename(dirpath)
    print("Directory name is : " + foldername)



def deploy_contract_with_data(user, description, license, link=""):
    from solcx import compile_source
    from web3 import Web3
    
    # Read in LUCE contract code
    with open(SOLIDITY_CONTRACT_FILE, 'r') as file:
        contract_source_code = file.read()
        
    # Compile & Store Compiled source code
    compiled_sol = compile_source(contract_source_code)

    # Extract full interface as dict from compiled contract
    contract_interface = compiled_sol['<stdin>:Dataset']

    # Extract abi and bytecode
    abi = contract_interface['abi']
    bytecode = contract_interface['bin']
    
    # Establish web3 connection

    # Obtin user
    current_user = user
    
    # Set sender
    w3.eth.defaultAccount = current_user.ethereum_public_key

    # Create contract blueprint
    Luce = w3.eth.contract(abi=abi, bytecode=bytecode)

    # Submit the transaction that deploys the contract
    tx_hash = Luce.constructor().transact()
    
    # Wait for the transaction to be mined, and get the transaction receipt
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    
    # Obtain address of freshly deployed contract
    contract_address = tx_receipt.contractAddress
    
    # Create python instance of deployed contract
    luce = w3.eth.contract(
    address=contract_address,
    abi=contract_interface['abi'],
    )
    
    # Store dataset information in contract
    tx_hash = luce.functions.publishData(description, link, license).transact()
    
    return contract_address

#### Initial Implementations
# These implementations make use of the Ganache pre-funded
# accounts. This is conveninent but doesn't scale well.
# To smoothen the later transition to a hosted node like Infura
# and using the official Ethereum testnet it it is preferable
# to have full control over the accounts.

def assign_address(user):
    # Establish web3 connection
    accounts = w3.eth.accounts
    # Obtain user model
    from django.contrib.auth import get_user_model
    User = get_user_model()
    # Obtain user count
    # The user count is used as a 'global counter'
    # to ensure each new user that registers is assigned
    # a new one of the pre-generated ganache acounts
    # I use this workaround as a proxy to track the
    # 'global state' of how many accounts are already
    # asigned.
    user_count = len(User.objects.all())
    idx = user_count-1
    # Assign web3 account to user
    current_user = user
    current_user.ethereum_public_key = accounts[idx]
    current_user.save()
    # Return user with address associated
    return current_user
	


"""

from web3 import Web3
import time
ip_address = "HTTP://192.168.0.4:8545"

w3 = Web3(Web3.HTTPProvider( ip_address))

import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# '/vagrant/luce_django/luce'
SOLIDITY_CONTRACT_FILE = BASE_DIR + '/utils/data/luce.sol'

#### WEB3 HELPER FUNCTIONS ####
# Helper functions used to make the code in assign_address_v3 easier to read

# Create faucet for pre-funding accounts
# NOTE: placing a private key here is obviously very unsafe
# We only do this for development usage. When transitioning 
# to Infura the faucet can be replaced with an API call instead.

# Private key (obtained via Ganache interface)
faucet_privateKey   = "0x4a2cb86c7d3663abebf7ab86a6ddc3900aee399750f35e65a44ecf843ec39116"
# Establish faucet account
faucet = w3.eth.account.privateKeyToAccount(faucet_privateKey)

def create_wallet():
    eth_account = w3.eth.account.create()
    return (eth_account)

def send_ether(amount_in_ether, recipient_address, sender_pkey=faucet.privateKey):
    amount_in_wei = w3.toWei(amount_in_ether,'ether');
    
    # Obtain sender address from private key
    sender_address = w3.eth.account.privateKeyToAccount(sender_pkey).address

    # How many transactions have been made by wallet?
    # This is required and prevents double-spending.
    # Same name but different from nonce in block mining.
    nonce = w3.eth.getTransactionCount(sender_address)
    
    # Specify transcation dictionary
    txn_dict = {
            'to': recipient_address,
            'value': amount_in_wei,
            'gas': 2000000,
            'gasPrice': w3.toWei('40', 'gwei'),
            'nonce': nonce,
            'chainId': 3
    }
    
    # IN THIS STEP THE PRIVATE KEY OF THE SENDER IS USED
    # Sign transaction
    def sign_transaction(txn_dict, sender_pkey):
        signed_txn = w3.eth.account.signTransaction(txn_dict, sender_pkey)
        return signed_txn
    signed_txn      = sign_transaction(txn_dict, sender_pkey)
    signed_txn_raw = signed_txn.rawTransaction
    
    
    # Send transaction & store transaction hash
    def send_raw_transaction(raw_transaction):
        txn_hash = w3.eth.sendRawTransaction(raw_transaction)
        return txn_hash
    txn_hash = send_raw_transaction(signed_txn_raw)

    # Check if transaction was added to blockchain 
    # time.sleep(5)     # Not needed on Ganache since our transactions are instantaneous
    txn_receipt = w3.eth.getTransactionReceipt(txn_hash)
    return txn_hash

def fund_wallet(recipient, amount = 100):
    send_ether(amount,recipient)



#### ASSIGN ADDRESS ####
# This script takes a Django user object as input and
# creates a fresh ethereum account for the user.
# It will also pre-fund the new account with some ether.

def assign_address_v3(user):
    # Establish web3 connection
    from web3 import Web3
    import time
    from hexbytes import HexBytes
    w3 = Web3(Web3.HTTPProvider( ip_address))
    accounts = w3.eth.accounts
    current_user = user

    # Create new web3 account
    eth_account = create_wallet()
    # Store public key and private key in user model
    current_user.ethereum_public_key = eth_account.address
    current_user.ethereum_private_key = eth_account.privateKey.hex() # this field is not implemented atm
    current_user.save()
    # Fund wallet
    fund_wallet(recipient = eth_account.address, amount = 100)
    print("Balance:", w3.eth.getBalance(current_user.ethereum_public_key)) # print balance to ensure funding took place
    # Return user, now with wallet associated
    return current_user


def deploy_contract_v3(private_key):
    from solcx import compile_source
    from web3 import Web3
    

    # Read in LUCE contract code
    with open(SOLIDITY_CONTRACT_FILE, 'r') as file: # Adjust file_path for use in Jupyter/Django
        contract_source_code = file.read()
    
    # Compile & Store Compiled source code
    compiled_sol = compile_source(contract_source_code)

    # Extract full interface as dict from compiled contract
    contract_interface = compiled_sol['<stdin>:Dataset']

    # Extract abi and bytecode
    abi = contract_interface['abi']
    bytecode = contract_interface['bin']
    
    # Establish web3 connection
    w3 = Web3(Web3.HTTPProvider( ip_address))
    
    #Obtain user so we know his address for the 'from' field
    user = w3.eth.account.privateKeyToAccount(private_key)
    
    # Construct raw transaction
    nonce = w3.eth.getTransactionCount(user.address)
    
    transaction = {
    'from': user.address,
    'gas': 2000000,
    'data': bytecode,
    'chainId': 3,
    'gasPrice': w3.toWei('40', 'gwei'),
    'nonce': nonce,
    }
    
    # Sign transaction
    signed_txn = w3.eth.account.signTransaction(transaction, private_key)
    
    # Deploy
    tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    
    # Wait for the transaction to be mined, and get the transaction receipt
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    
    # Obtain address of freshly deployed contract
    contractAddress = tx_receipt.contractAddress
    
    return contractAddress


# Auxilary function to support interaction with existing smart contract
def compile_and_extract_interface():
    from solcx import compile_source
    
    # Read in LUCE contract code
    with open(SOLIDITY_CONTRACT_FILE, 'r') as file: # Adjust file_path for use in Jupyter/Django
        contract_source_code = file.read()
        
    # Compile & Store Compiled source code
    compiled_sol = compile_source(contract_source_code)

    # Extract full interface as dict from compiled contract
    contract_interface = compiled_sol['<stdin>:Dataset']

    # Extract abi and bytecode
    abi = contract_interface['abi']
    bytecode = contract_interface['bin']
    
    # Create dictionary with interface
    d = dict()
    d['abi']      = abi
    d['bytecode'] = bytecode
    d['full_interface'] = contract_interface
    return(d)


def publish_data_v3(provider_private_key, contract_address, description="Description", license=3, link="void"):
    from web3 import Web3
    
    # Compile Luce contract and obtain interface
    d = compile_and_extract_interface()
    
    # Establish web3 connection
    w3 = Web3(Web3.HTTPProvider( ip_address))
    
    # Obtain user so we know his address for the 'from' field
    private_key = provider_private_key
    user = w3.eth.account.privateKeyToAccount(private_key)
    
    # Obtain contract address & instantiate contract
    contract_address = contract_address
    luce = w3.eth.contract(address=contract_address, abi=d['abi'])
    
    # Construct raw transaction
    nonce = w3.eth.getTransactionCount(user.address)
    txn_dict = {
    'gas': 2000000,
    'chainId': 3,
    'gasPrice': w3.toWei('40', 'gwei'),
    'nonce': nonce,
    }
    
    luce_txn = luce.functions.publishData(description,link,license).buildTransaction(txn_dict)
    
    # Sign transaction
    signed_txn = w3.eth.account.signTransaction(luce_txn, private_key)
    
    # Deploy
    tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    
    # Wait for the transaction to be mined, and get the transaction receipt
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    
    return tx_receipt

def add_requester_v3(requester_private_key, contract_address, license=3, purpose_code=3):
    from web3 import Web3
    

    # Compile Luce contract and obtain interface
    d = compile_and_extract_interface()
    
    # Establish web3 connection
    w3 = Web3(Web3.HTTPProvider( ip_address))
    
    # Obtain user so we know his address for the 'from' field
    private_key = requester_private_key
    user = w3.eth.account.privateKeyToAccount(private_key)
    
    # Obtain contract address & instantiate contract
    contract_address = contract_address
    luce = w3.eth.contract(address=contract_address, abi=d['abi'])
    
    # Construct raw transaction
    nonce = w3.eth.getTransactionCount(user.address)
    txn_dict = {
    'gas': 2000000,
    'chainId': 3,
    'gasPrice': w3.toWei('40', 'gwei'),
    'nonce': nonce,
    }
    
    license_type = license
    # Obtain license from smart contract
    license_type = luce.functions.getLicence().call()
    luce_txn = luce.functions.addDataRequester(purpose_code,license_type).buildTransaction(txn_dict)
    
    # Sign transaction
    signed_txn = w3.eth.account.signTransaction(luce_txn, private_key)
    
    # Deploy
    tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    
    # Wait for the transaction to be mined, and get the transaction receipt
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    
    return tx_receipt

def update_contract_v3(provider_private_key, contract_address, description="Updated Description", link="void"):
    from web3 import Web3
    
    # Compile Luce contract and obtain interface
    d = compile_and_extract_interface()
    
    # Establish web3 connection
    w3 = Web3(Web3.HTTPProvider( ip_address))
    
    # Obtain user so we know his address for the 'from' field
    private_key = provider_private_key
    user = w3.eth.account.privateKeyToAccount(private_key)
    
    # Obtain contract address & instantiate contract
    contract_address = contract_address
    luce = w3.eth.contract(address=contract_address, abi=d['abi'])
    
    # Construct raw transaction
    nonce = w3.eth.getTransactionCount(user.address)
    txn_dict = {
    'gas': 2000000,
    'chainId': 3,
    'gasPrice': w3.toWei('40', 'gwei'),
    'nonce': nonce,
    }
    
    luce_txn = luce.functions.updateData(description,link).buildTransaction(txn_dict)
    
    # Sign transaction
    signed_txn = w3.eth.account.signTransaction(luce_txn, private_key)
    
    # Deploy
    tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    
    # Wait for the transaction to be mined, and get the transaction receipt
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    
    return tx_receipt




#### Initial Implementations
# These implementations make use of the Ganache pre-funded
# accounts. This is conveninent but doesn't scale well.
# To smoothen the later transition to a hosted node like Infura
# and using the official Ethereum testnet it it is preferable
# to have full control over the accounts.

def assign_address(user):
    # Establish web3 connection
    from web3 import Web3
    w3 = Web3(Web3.HTTPProvider( ip_address))
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



def deploy_contract(user):
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
    w3 = Web3(Web3.HTTPProvider( ip_address))

    # Obtain user
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
    contractAddress = tx_receipt.contractAddress

    return contractAddress


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
    w3 = Web3(Web3.HTTPProvider( ip_address))

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

    # Wallet address
    faucet.address       = "0x92D44e8579620F2Db88A12E70FE38e8CDB3541BA"
    # Private key (from Ganache interface)
    faucet.pkey   = "0x4a2cb86c7d3663abebf7ab86a6ddc3900aee399750f35e65a44ecf843ec39116"

    # Define a function to send ether

    def send_ether(amount_in_ether, recipient_address, sender_address = faucet.address, sender_pkey=faucet.pkey):
        amount_in_wei = w3.toWei(amount_in_ether,'ether');

        # How many transactions have been made by wallet?
        # This is required and prevents double-spending.
        # Different from nonce in block mining.
        nonce = w3.eth.getTransactionCount(sender_address)
        
        # Specify transcation dictionary
        txn_dict = {
                'to': recipient_address,
                'value': amount_in_wei,
                'gas': 2000000,
                'gasPrice': w3.toWei('40', 'gwei'),
                'nonce': nonce,
                'chainId': 3
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

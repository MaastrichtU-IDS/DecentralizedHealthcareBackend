from web3 import Web3
from eth_abi import decode_abi

w3 = Web3(Web3.HTTPProvider('HTTP://127.0.0.1:7545'))

block = w3.eth.get_block(134, full_transactions=True)

transactions = block.transactions

first_transaction = transactions[0]
# print(dir(first_transaction))
contract_address = '0x44e802A2adE7345618e1acf67b3C95fd47278Fa6'
contract_address = '0x44e802A2adE7345618e1acf67b3C95fd47278Fa6'

contract = w3.eth.contract(address = contract_address)
# print(contract.all_functions())
print(contract)

# input_data = first_transaction.input

# contract.decode_function_input(input_data)
# input_types = abi['inputs']

# decoded_input = decode_abi(input_types, bytes.fromhex(input_data[2:]))

# print(decoded_input)
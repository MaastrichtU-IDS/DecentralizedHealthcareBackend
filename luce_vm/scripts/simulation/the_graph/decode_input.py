from web3 import Web3
from eth_abi import decode_abi

# 初始化web3实例
w3 = Web3(Web3.HTTPProvider('HTTP://127.0.0.1:7545'))

# 交易哈希
tx_hash = '0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef'

# 获取交易
tx = w3.eth.get_transaction(tx_hash)

# 获取方法ABI
abi = '...'

# 解码输入
input_data = tx.input
input_types = abi['inputs']
decoded_input = decode_abi(input_types, bytes.fromhex(input_data[2:]))

print(decoded_input)

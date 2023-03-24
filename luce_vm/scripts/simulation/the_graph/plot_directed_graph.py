from web3 import Web3
import networkx as nx
import matplotlib.pyplot as plt

w3 = Web3(Web3.HTTPProvider('HTTP://127.0.0.1:7545'))

# 获取以太坊最新区块号
latest_block_number = w3.eth.block_number

print(latest_block_number)
# 从最新区块号向后遍历所有区块并获取所有交易数据
all_txs = []
for block_number in range(latest_block_number):
    block = w3.eth.get_block(block_number, full_transactions=True)
    for tx in block.transactions:
        all_txs.append(tx)

# print(len(all_txs))



# 创建一个空的有向图
G = nx.DiGraph()

# 遍历所有交易，将交易的发送方和接收方添加到图中
# print(len(all_txs))
for tx in all_txs:
    if (tx['from'] is None) or (tx['to'] is None):
        continue
    G.add_edge(tx['from'], tx['to'])

# 绘制交易图
pos = nx.spring_layout(G, k=0.15, iterations=20)

# We can customize with `node_size` and `width`, refer to `draw_networkx`
nx.draw(G, pos, node_size=50, with_labels=False, font_weight='bold', arrows=False)
plt.show()


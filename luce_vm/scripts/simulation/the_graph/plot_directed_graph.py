from web3 import Web3
import networkx as nx
import matplotlib.pyplot as plt
import random

w3 = Web3(Web3.HTTPProvider('HTTP://127.0.0.1:7545'))


def get_all_txs():

    # 获取以太坊最新区块号
    latest_block_number = w3.eth.block_number
    # print(latest_block_number)

    # print(latest_block_number)
    # 从最新区块号向后遍历所有区块并获取所有交易数据
    all_txs = []
    for block_number in range(latest_block_number + 1):
        # print(block_number)
        block = w3.eth.get_block(block_number, full_transactions=True)
        for tx in block.transactions:
            all_txs.append(tx)

    return all_txs


# print(len(all_txs))


def check_blocks(blocks):
    for b in blocks:
        block = w3.eth.get_block(b, full_transactions=True)
        # print(b72.transactions)

        for tx in block.transactions:
            tx_hash = w3.toHex(tx['hash'])
            receipt = w3.eth.get_transaction_receipt(tx_hash)
            print(receipt)
            print("********")
    # print(tx_hash)
    # print(tx['from'])
    # print(tx['to'])
    # print(tx['contractAddress'])


blocks = [86, 87, 88, 89]

# check_blocks(blocks)
# 创建一个空的有向图

# 遍历所有交易，将交易的发送方和接收方添加到图中
# print(len(all_txs))


def handle_receipt(G, receipt):
    if receipt['to'] is None:
        G.add_edge(
            receipt['from'],
            receipt['contractAddress'],
        )
    else:
        G.add_edge(
            receipt['from'],
            receipt['to'],
        )


def handle_receipt(G, receipt, address, count=0):
    edge_list = []
    if receipt['to'] is None:
        if receipt['contractAddress'] == address:

            # print(receipt['from'])

            edge = (receipt['from'], receipt['contractAddress'], {'w': count})
            # print(edge)

            edge_list.append(edge)
            count = count + 1

    else:
        if receipt['to'] == address:

            edge = (receipt['from'], receipt['to'], {'w': count})
            # print(edge)
            edge_list.append(edge)
            count = count + 1

    G.add_edges_from(edge_list)


def transaction_graph(all_txs, address=None):
    G = nx.MultiGraph()
    count = 0
    edge_list = []
    for tx in all_txs:
        tx_hash = w3.toHex(tx['hash'])
        receipt = w3.eth.get_transaction_receipt(tx_hash)

        # build a transaction graph with all transactions
        if address is None:
            handle_receipt(G, receipt)

        # build a transaction graph based one a specific account
        else:
            for a in address:
                handle_receipt(G, receipt, a, count=count)

    return G


# 绘制交易图
all_txs = get_all_txs()
G = transaction_graph(all_txs,
                      address=[
                          "0xc7717427eEdA72E31C2a4069F492F783ac49fa5b",
                          "0xceCebaf5d763574e83faB550ec0655dAFf8dC494"
                      ])
pos = nx.spring_layout(G, k=0.15, iterations=20)
# pos = nx.random_layout(G)

edges = G.edges()
# weights = [G[u][v]['w'] for u, v in edges]
weights = nx.get_edge_attributes(G, 'w')
# print(weights.keys())
# for w in weights:
# print(edges)
# nodes = G.nodes()
# labels = []
# for n in nodes:
#     # print(n[-7:-1])
#     labels.append(n[-7:-1])

# print(labels)
nx.draw_networkx_nodes(G, pos)
# print(G.nodes())

ax = plt.gca()
count = 0
for e in edges:
    count = count + 1
    ax.annotate(
        "",
        xy=pos[e[0]],
        xycoords='data',
        xytext=pos[e[1]],
        textcoords='data',
        arrowprops=dict(
            arrowstyle="-",
            color="0.5",
            shrinkA=5,
            shrinkB=5,
            patchA=None,
            patchB=None,
            connectionstyle="arc3,rad=rrr".replace('rrr',
                                                   str(random.random() - 0.5)),
        ),
    )

# colors = [G[u][v]['color'] for u, v in edges]
# weights = [G[u][v]['weight'] for u, v in edges]

# print(weights)

# curved_edges = [edge for edge in G.edges() if reversed(edge) in G.edges()]
# print(G.edges())

# print(len(curved_edges))
# straight_edges = list(set(G.edges()) - set(curved_edges))

# nx.draw(
#     G,
#     pos,
#     # edge_color=colors,
#     node_size=50,
#     with_labels=False,
#     font_weight='bold',
#     # width=weights,
#     # arrows=False
# )
# nx.draw_networkx_labels(G, pos)
plt.show()

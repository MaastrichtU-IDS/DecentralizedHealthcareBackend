from web3 import Web3
import networkx as nx
import matplotlib.pyplot as plt
import random

w3 = Web3(Web3.HTTPProvider('HTTP://127.0.0.1:7545'))


def get_all_txs():

    # 获取以太坊最新区块号
    latest_block_number = w3.eth.block_number
    print("latest block number: ", latest_block_number)
    # print(latest_block_number)

    # print(latest_block_number)
    # 从最新区块号向后遍历所有区块并获取所有交易数据
    all_txs = []
    for block_number in range(latest_block_number - 64,
                              latest_block_number + 1):
        # print(block_number)
        print("retrieve block: ", block_number)
        block = w3.eth.get_block(block_number, full_transactions=True)
        for tx in block.transactions:
            all_txs.append(tx)

    return all_txs


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
    # print(receipt)
    edge_list = []
    if receipt['to'] is None:
        print("to is none")
        if receipt['contractAddress'] == address:

            edge = (receipt['from'], receipt['contractAddress'], {'w': count})

            edge_list.append(edge)
            count = count + 1

    else:
        if receipt['to'] == address:
            print(receipt)
            edge = (receipt['from'], receipt['to'], {'w': count})

            edge_list.append(edge)
            count = count + 1

    G.add_edges_from(edge_list)


def transaction_graph(all_txs, address=None):

    # G = nx.MultiGraph()
    G = nx.DiGraph()
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
                if receipt['from'] == a or receipt['to'] == a:

                    print(receipt)
                    print("")
                    # handle_receipt(G, receipt, a, count=count)
                # print(receipt)
                handle_receipt(G, receipt, a, count=count)

    return G


# 绘制交易图
print("draw graph")
print("**********")
print("get all txs")
all_txs = get_all_txs()

target_data = {
    "provider":
    "0x682779a69B18db2efaBFB397418b565ae7588018",
    "contract_address":
    "0xB3B12F4fa60E04B41D8eaebBf785105Dc3bf67A2",
    "requester": [
        "0x37ad04f21b245aD95784F833E14f8cfB51632908",
        "0xdFa15F97d217512eE82cbc8AD11C457e251aBdad"
    ]
}

# G = nx.DiGraph()

# edge_list = []

# for tx in all_txs:
#     tx_hash = w3.toHex(tx['hash'])
#     receipt = w3.eth.get_transaction_receipt(tx_hash)

# if receipt["from"] == target_data["provider"]:

# print(receipt)

G = transaction_graph(all_txs,
                      address=[
                          "0x682779a69B18db2efaBFB397418b565ae7588018",
                          "0xB3B12F4fa60E04B41D8eaebBf785105Dc3bf67A2",
                          "0x37ad04f21b245aD95784F833E14f8cfB51632908",
                          "0xdFa15F97d217512eE82cbc8AD11C457e251aBdad"
                      ])

nx.draw(G, with_labels=True)
plt.show()

# pos = nx.spring_layout(G, k=0.15, iterations=20)
# # pos = nx.random_layout(G)

# edges = G.edges()
# # weights = [G[u][v]['w'] for u, v in edges]
# weights = nx.get_edge_attributes(G, 'w')

# # print(labels)
# nx.draw_networkx_nodes(G, pos)
# # print(G.nodes())

# ax = plt.gca()
# count = 0
# for e in edges:
#     count = count + 1
#     ax.annotate(
#         "",
#         xy=pos[e[0]],
#         xycoords='data',
#         xytext=pos[e[1]],
#         textcoords='data',
#         arrowprops=dict(
#             arrowstyle="-",
#             color="0.5",
#             shrinkA=5,
#             shrinkB=5,
#             patchA=None,
#             patchB=None,
#             connectionstyle="arc3,rad=rrr".replace('rrr',
#                                                    str(random.random() - 0.5)),
#         ),
#     )

# plt.show()

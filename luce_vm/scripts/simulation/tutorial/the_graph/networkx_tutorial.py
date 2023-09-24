import networkx as nx
import matplotlib.pyplot as plt

DG = nx.DiGraph()
DG.add_edges_from([(1, 2), (1, 3), (2, 3), (3, 4), (4, 5), (5, 1)])

nx.draw(DG, with_labels=True)
plt.show()
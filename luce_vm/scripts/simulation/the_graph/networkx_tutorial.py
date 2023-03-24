import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph(day ="Friday")



nx.draw(G, with_labels=True)
plt.show()
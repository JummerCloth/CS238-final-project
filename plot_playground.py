import networkx as nx
import matplotlib.pyplot as plt

# Given edge means
times_mean = {
    ('A', 'B'): 1.2,
    ('A', 'C'): 10.0,
    ('B', 'D'): 1.5,
    ('B', 'E'): 2.7,
    ('C', 'E'): 2.4,
    ('C', 'F'): 2.0,
    ('D', 'G'): 13.0,
    ('E', 'G'): 0.3,
    ('F', 'G'): 2.9
}

# Create a graph (use directed if direction matters, else Graph)
G = nx.Graph()

# Add edges with weights
for (u, v), w in times_mean.items():
    G.add_edge(u, v, weight=w)

# Use kamada_kawai_layout which tries to place nodes so that pairwise distances 
# approximate shortest path distances in the graph.
pos = nx.kamada_kawai_layout(G, weight='weight')

# Draw the nodes
nx.draw_networkx_nodes(G, pos, node_size=1500, node_color='lightblue')

# Draw the edges
nx.draw_networkx_edges(G, pos, edge_color='gray', arrows=False)

# Draw the labels for the nodes
nx.draw_networkx_labels(G, pos, font_size=14, font_family='sans-serif')

# Extract edge labels from graph for display
edge_labels = {(u, v): f"{w}" for (u, v, w) in G.edges(data='weight')}

# Draw edge labels
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', font_size=12)

plt.title("Graph Visualization of Pupper PlayGround")
plt.axis('off')
plt.tight_layout()
plt.show()

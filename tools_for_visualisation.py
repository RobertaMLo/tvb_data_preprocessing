import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


def plot_your_graph(connectivity_matrix, region_labels, title, ncol, ecol, figdim):
    """
    To plot the connectivity as a graph using networkx.
    Input:
        connectivty_matrix  = float 2D array (e.g. structural connectivty)
        region_labels       = 'string', list with the label for the graph (e.g., the regions)
        title               = 'string', title of the plot
        ncol                = 'string', color for nodes
        ecol                = 'string', color for edges
        figdim              = 'int' 1x2 tuple, size of the figure
    :return: []
    """

    # Create a graph
    G = nx.Graph()

    # Add nodes with labels and sizes based on node strengths
    node_strengths = np.sum(connectivity_matrix, axis=1)
    for label, strength in zip(region_labels, node_strengths):
        G.add_node(label, size=strength)

    # Add edges with weights based on connectivity matrix
    for i in range(len(region_labels)):
        for j in range(len(region_labels)):
            if i != j:  # Exclude self-loops for better visualization
                G.add_edge(region_labels[i], region_labels[j], weight=connectivity_matrix[i, j])

    # Use Kamada-Kawai layout for the network
    pos = nx.kamada_kawai_layout(G)

    # Set node sizes based on strengths
    node_sizes = [data['size'] * 100 for _, data in G.nodes(data=True)]

    # Set edge widths based on weights
    edge_widths = [data['weight'] * 5 for _, _, data in G.edges(data=True)]

    # Plotting
    plt.figure(figsize=figdim)
    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color=ncol, alpha=0.8)
    nx.draw_networkx_edges(G, pos, width=edge_widths, edge_color=ecol, alpha=0.5)
    nx.draw_networkx_labels(G, pos, font_size=8, font_color='black', font_weight='bold')
    plt.title(title)
    plt.show()


def compute_and_plot_my_bars(connectivity_matrix, sum_axis, region_labels, title, xlab, ylab, col, figdim):
    """
        To plot the connectivity as a bar chart.
        Input:
            connectivity_matrix  = float 2D array (e.g. structural connectivty)
            sum_axis             = 'int', axis along which computing the sum
            region_labels        = 'string', list with the label for the graph (e.g., the regions)
            title                = 'string', title of the plot
            xlab                 = 'string', label for x-axis
            ylab                 = 'string', label for yaxis
            col                  = 'string', color for the bars
            figdim               = 'int' 1x2 tuple, size of the figure
        :return: []
        """

    # Calculate the sum of incoming connections for each region
    incoming_connections_sum = np.sum(connectivity_matrix, axis=sum_axis)

    plt.figure(figsize=figdim)
    plt.bar(region_labels, incoming_connections_sum, color=col)
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    plt.title(title)
    plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better visibility
    plt.show()

    return incoming_connections_sum




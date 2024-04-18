import numpy as np
from scipy import stats as st
import networkx as nx
import matplotlib.pyplot as plt


def load_matrix_and_labels(con_name, lab_name, delimiter_conn_file):
    """
    Load the connectivtity data
    con_name = 'String', name of the connectivity matrix file (should be a txt)
    lab_name = 'String', name of the labels file. Usually it is stored with also centres coordinates so loading restricted to col0
    N.B. _name required also the PATH
    :return: conn matrix, labels
    """

    conn_mat = np.loadtxt(con_name, delimiter = delimiter_conn_file)
    centers = np.loadtxt(lab_name, dtype=str)
    region_labels=centers[:,0]

    return conn_mat, region_labels



def plot_your_matrix(matrix, labels, step_labels, title, cbar_name, cmap_type, figdim):

    """
    To plot the connectivity as a graph using networkx.
    Input:
        matrix              = float 2D array (e.g. structural connectivty)
        labels              = 'string', list with the label for the graph (e.g., the regions)
        step_labels         = 'int', step between regions labels
        title               = 'string', title of the plot
        cbar_name           = 'string', name of the color bar
        cmap                = 'string', cmap name in matplotlib
        figdim              = 'int' 1x2 tuple, size of the figure
    :return: []
    """
    fig, axs = plt.subplots(nrows=1, ncols=1, figsize=figdim)
    axs.set_title(title)
    pos0 = axs.imshow(matrix, cmap = cmap_type, vmin=np.min(matrix), vmax=np.max(matrix), origin= 'upper')
    cb0 = fig.colorbar(pos0, ax=axs, anchor=(0, 0.3), shrink=0.7)
    cb0.set_label(cbar_name, fontsize=12)
    axs.set_xticks(np.arange(0, len(labels[0:-1]), step_labels), labels[0:-1:step_labels], fontsize=9, rotation=90)
    axs.set_yticks(np.arange(0, len(labels[0:-1]), step_labels), labels[0:-1:step_labels], fontsize=9)
    plt.show()



def plot_2_matrices(matrix, labels, step_labels, title, cbar_name, cmap,
                        matrix1, labels1, step_labels1, title1, cbar_name1, cmap1,
                        figdim):

    """
    To plot the connectivity as a graph using networkx.
    Input:
        matrix              = float 2D array (e.g. structural connectivty)
        labels              = 'string', list with the label for the graph (e.g., the regions)
        step_labels         = 'int', step between regions labels
        title               = 'string', title of the plot
        cbar_name           = 'string', name of the color bar
        cmap                = 'string', cmap name in matplotlib

        input1 analogous to the ones above

        figdim              = 'int' 1x2 tuple, size of the figure
    :return: []
    """
    fig, axs = plt.subplots(nrows=1, ncols=2, figsize=figdim)
    axs[0].set_title(title)
    pos0 = axs[0].imshow(matrix, cmap = cmap, vmin=np.min(matrix), vmax=np.max(matrix) *1e-1, origin= 'upper')
    cb0 = fig.colorbar(pos0, ax=axs[0], anchor=(0, 0.3), shrink=0.7)
    cb0.set_label(cbar_name, fontsize=12)
    axs[0].set_xticks(np.arange(0, len(labels[0:-1]), step_labels), labels[0:-1:step_labels], fontsize=9, rotation=90)
    axs[0].set_yticks(np.arange(0, len(labels[0:-1]), step_labels), labels[0:-1:step_labels], fontsize=9)

    axs[1].set_title(title1)
    pos1 = axs[1].imshow(matrix1, cmap = cmap1, vmin=np.min(matrix), vmax=np.max(matrix)*1e-1, origin= 'upper')
    cb1 = fig.colorbar(pos1, ax=axs[1], anchor=(0, 0.3), shrink=0.7)
    cb1.set_label(cbar_name1, fontsize=12)
    axs[1].set_xticks(np.arange(0, len(labels1[0:-1]), step_labels1), labels1[0:-1:step_labels1], fontsize=9, rotation=90)
    axs[1].set_yticks(np.arange(0, len(labels1[0:-1]), step_labels1), labels1[0:-1:step_labels1], fontsize=9)
    plt.show()


def plot_your_graph(connectivity_matrix, region_labels, layout, title, ncol, ecol, figdim):
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
    if layout == 'kamada':
        pos = nx.kamada_kawai_layout(G)
    elif layout == 'circular':
        pos = nx.circular_layout(G)
    else:
        pos = nx.random_layout(G)
        print('Warning: random layout. Please, if you want to select one, choose between kamada and circular')
    

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


def compute_and_plot_my_bars(connectivity_matrix, metrics_axis, metrics_name, region_labels, title, xlab, ylab, col, figdim):
    """
        To plot the connectivity as a bar chart.
        Input:
            connectivity_matrix  = float 2D array (e.g. structural connectivty)
            metrics_axis         = 'int', axis along which computing the metrix
            metrics_name         = 'string', choose between 'mean', 'sum', 'mode', 'median'
            region_labels        = 'string', list with the label for the graph (e.g., the regions)
            title                = 'string', title of the plot
            xlab                 = 'string', label for x-axis
            ylab                 = 'string', label for yaxis
            col                  = 'string', color for the bars
            figdim               = 'int' 1x2 tuple, size of the figure
        :return: []
        """

    # Calculate the sum of incoming connections for each region
    if metrics_name == 'mean':
        incoming_connections = np.sum(connectivity_matrix, axis=metrics_axis)
    elif metrics_name =='sum':
        incoming_connections = np.mean(connectivity_matrix, axis=metrics_axis)
    elif metrics_name == 'median':
        incoming_connections = np.median(connectivity_matrix, axis=metrics_axis)
    elif metrics_name == 'mode':
        incoming_connections = st.mode(connectivity_matrix, axis=metrics_axis)
    else:
        print('Metric not available. Please choose amongst: mean, sum, median, mode')



    plt.figure(figsize=figdim)
    plt.bar(region_labels, incoming_connections, color=col)
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    plt.title(title)
    plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better visibility
    plt.show()

    return incoming_connections

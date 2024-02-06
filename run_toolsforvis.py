
""" Trial code to test the visualisation library """
from tools_for_visualisation import *

connectivity_matrix = np.random.rand(10, 10)
# Sample list of region labels (replace this with your actual labels)
region_labels = ['Region A', 'Region B', 'Region C', 'Region D', 'Region E', 'Region F', 'Region G', 'Region H', 'Region I', 'Region J']
ncol = 'm'
ecol = 'grey'
figdim = (10,10)

#plot_your_graph(connectivity_matrix,region_labels,'prova', ncol, ecol, figdim)


compute_and_plot_my_bars(connectivity_matrix, 1, region_labels, 'var', 'c', 'y', 'm', figdim)
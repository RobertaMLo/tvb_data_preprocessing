
import numpy as np
from curation_SC import fix_fromdentate2crblctx, mapping_parallel_frog, compute_parallel, merge_SC_all_radial
from tools_for_visualisation import load_matrix_and_labels, plot_your_matrix, plot_2_matrices

"""
root_path = '/Users/robertalorenzi/PycharmProjects/IntegrationMFCRBL/'
SC_path_cur = root_path + 'Mouse/tvb_model_reference/data/Mouse_512/Conn_Curation_100307_SC/weights.txt'
labels_path = root_path + 'Mouse/tvb_model_reference/data/Mouse_512/Conn_Curation_100307_SC/centres.txt'
SC_path_std = root_path + 'Mouse/tvb_model_reference/data/Mouse_512/Conn_Count_dirCRBL_100307_SC/weights.txt'
"""
SC_path_cur = '/Users/robertalorenzi/Desktop/prova_CPC_sbagliato_includeDentate/atlas_SC_count_dirCb_NORM.txt'
#Matteo_prova100307/atlas_SC_count_dirCb_NORM.txt'

SC_path_std = '/Users/robertalorenzi/Desktop/SC4TVB/Conn_Count_dirCRBL/weights_Count_dirCRBL.txt'
labels_path = '/Users/robertalorenzi/Desktop/SC4TVB/Conn_Count_dirCRBL/centres_brain_MNI.txt'

SC_cur, labels = load_matrix_and_labels(SC_path_cur, labels_path, delimiter_conn_file=' ')
SC_std, _ = load_matrix_and_labels(SC_path_std, labels_path, delimiter_conn_file=' ')

plot_your_matrix(SC_cur, labels, 5, title='SC', cbar_name='weights', cmap_type='jet', figdim=(10, 10))


# # NESTED PROCEDURE
# # output of one function is the input for the following one

SC = merge_SC_all_radial(SCall=SC_cur, SCrad=SC_std, idxdent=[103, 104, 105, 113, 114, 115])
#plot_your_matrix(SC_cur, labels, 3, title='SC', cbar_name='weights', cmap_type='jet', figdim=(10, 10))

# SC = np.random.rand(6, 6) *100 #For quick test if it works

SC_dL = fix_fromdentate2crblctx(SC, [103, 104, 105])
#From Right to Left
RL = 10
SC_d = fix_fromdentate2crblctx(SC_dL, [103 + RL, 104 + RL, 105 + RL])

# # Output = mapping of where parallel exists, other values = 0
SC_map = mapping_parallel_frog(SC_d)

Kp = (907.9*70 + 1463*99 + 484.4*299 + 735.4*147 ) / (70 + 99 + 299 + 247)      #media pesata per la numerosità di cellule
Kp = 0.2 * (1e-3 * Kp)
# # Commento a sopra:
# # metto 1e-3 perchè sono un botto... Kp come sopra circa 600... Lo motivo come scaling micro-milli
# # 0.2 perchè ho sempre preso il 20%

# # Output = SC with ONLY parallel fibers, and other values = 0
SC_p = compute_parallel(SC_map, Kp)

# # Final Output as sum of dentate and parallel processing
SC_curated = SC_d + SC_p
#plot_your_matrix(SC_curated[93:,93:]/np.sum(SC_curated[93:,93:], axis=0), labels[93:], 1, title='SC', cbar_name='weights', cmap_type='jet', figdim=(10, 10))

# # normalized on incoming connection (TO is on rows, axis = 0)
# # doing it both for curation and standard
#norm_SC_curated = SC_curated/np.sum(SC_curated, axis=0)
#norm_SC_curated_crbl = norm_SC_curated[93:, 93:]
norm_SC_curated = SC_curated/np.max(SC_curated)
norm_SC_curated_crbl = norm_SC_curated[93:, 93:]

#norm_SC_std = SC_std/np.sum(SC_std, axis=0)
#norm_SC_std_crbl = norm_SC_std[93:, 93:]
norm_SC_std = SC_std/np.max(SC_std)
norm_SC_std_crbl = norm_SC_std[93:, 93:]

plot_2_matrices(matrix=SC_std, labels=labels, step_labels=3,
                title='Whole brain SC - standard', cbar_name='weigths', cmap='jet',
                matrix1=SC_std[93:,93:], labels1=labels[93:], step_labels1=1,
                title1='Cerebellar SC - standard', cbar_name1='weigths', cmap1='jet',
                figdim=(16, 8) )

plot_2_matrices(matrix=SC_curated, labels=labels, step_labels=3,
                title='Whole brain SC - curated ', cbar_name='weigths', cmap='jet',
                matrix1=SC_curated[93:,93:], labels1=labels[93:], step_labels1=1,
                title1='Cerebellar SC - curated', cbar_name1='weigths', cmap1='jet',
                figdim=(16, 8) )

plot_your_matrix(SC_curated-SC_std, labels, 1, title='Difference SC curated - SC standard', cbar_name='weights', cmap_type='jet', figdim=(10, 10))

plot_2_matrices(matrix=norm_SC_curated, labels=labels, step_labels=3,
                title='Whole brain SC - curation', cbar_name='weigths', cmap='jet',
                matrix1=norm_SC_curated_crbl, labels1=labels[93:], step_labels1=1,
                title1='Cerebellar SC - curation', cbar_name1='weigths', cmap1='jet',
                figdim=(16, 8) )

print('done')

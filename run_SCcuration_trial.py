
import numpy as np
from tools_for_curation_SC import fix_fromdentate2crblctx, mapping_parallel, merge_SC_all_radial, read_txt_vol, save_curated_matrix
from tools_for_visualisation import load_matrix_and_labels, plot_your_matrix, plot_2_matrices
import argparse
import os


def main():


    parser = argparse.ArgumentParser(description="\
                                    SC curation process.\
                                    Script for implementing Cerebellar SC curation by integrating parallel fibers.\
                                    Usage: run_SCcuration_trial SUB_ID [options]\
                                     ")
    
    parser.add_argument("SUB_ID", help="Subject ID")
    parser.add_argument("--prot_folder", help="Protocol folder", default='/media/bcc/Volume/Analysis/Roberta/HCP_TVBmm_30M')
    parser.add_argument("--labels_path", help="file with the cntres of the labels", default='/home/bcc/matlab/Atlases/Parcellation/4TVB_centres32_brain_MNI.txt')
    parser.add_argument("--conn_folder_name", help="Standard connectome", default='Connectome')
    parser.add_argument("--connDCN_folder_name", help="All connectome - for dentate", default='Connectome_all')
    parser.add_argument("--plot_mat", help="boolean to plot matrices", type = bool, default=False)



    args = parser.parse_args()



    # # LOADING ============================================================================================================
    # # ====================================================================================================================
    # # SC Matrices --------------------------------------------------------------------------------------------------------
    SUB_ID =  args.SUB_ID
    
    labels_path = args.labels_path
    prot_folder = args.prot_folder
    #prot_folder = 'HCP_TVBmm/'


    conn_folder = args.conn_folder_name
    conn_folder2 = args.connDCN_folder_name
   
    SUB_DIR = prot_folder+'/'+SUB_ID+'/T1w/'

    SC_path = SUB_DIR + conn_folder + '/atlas_SC_count_dirCb_NORM.txt'
    SC_path_DCN = SUB_DIR + conn_folder2 + '/atlas_SC_count_dirCb_NORM.txt'

    # # Volumes ------------------------------------------------------------------------------------------------------------
    Lob_vols = SUB_DIR + 'Lobules.txt'
    CRBL = SUB_DIR + 'CRBL_vol.txt'
    ICV = SUB_DIR + 'ICV.txt'
    # first output = volume in voxels not needed here.
    _, lob_vols_mm = read_txt_vol(Lob_vols)
    _, CRBL_vols_mm = read_txt_vol(CRBL)
    _, ICV_mm = read_txt_vol(ICV)
    SC_subj, labels = load_matrix_and_labels(SC_path, labels_path, delimiter_conn_file=' ')
    SC_subj_all, labels = load_matrix_and_labels(SC_path_DCN, labels_path, delimiter_conn_file=' ')
    #plot_your_matrix(SC_subj, labels, 3, title='SC', cbar_name='weights', cmap_type='jet', figdim=(10, 10))

    # # CURATION  ==========================================================================================================
    # # ====================================================================================================================
    # # LOAD AND VIEW THE MATRIX ---------------------------------------------------------------------------

    # # 0) INITIALIZATION OF THE CEREBELLAR SC
    SC_curated = np.ones_like(SC_subj) * SC_subj #I'm gonna keep the cerebrum and incoming connections to dentate
    SC_curated[93:, 93:] = 0

    # # 1) CURATION OF CONNECTIONS FROM DENTATE TO CRBL CORTEX ON THE STANDARD SC
    right_to_left = 10
    dent_index = [103, 104, 105, 103+right_to_left, 104+right_to_left, 105+right_to_left]
    # # 1.1 to dcn from cerebellar cortex as detected in tractography
    #SC_curated[dent_index, 93:] = SC_subj[dent_index, 93:]
    SC_curated[dent_index, 93:] = SC_subj_all[dent_index, 93:]


    #plot_your_matrix(SC_curated[93:, 93:], labels[93:], 1, title='SC', cbar_name='weights', cmap_type='jet', figdim=(10, 10))
    # # 1.2 to cortex from dcn reduced of 90%
    #SC_outDent = fix_fromdentate2crblctx(SC_subj, dent_index)

    SC_outDent = fix_fromdentate2crblctx(SC_subj_all, dent_index)  # Temporaty matrices, I am taking nly from dent to crbl cortex
    SC_curated[93:, dent_index] = SC_outDent[93:, dent_index]
    #plot_your_matrix(SC_curated[93:, 93:], labels[93:], 1, title='SC', cbar_name='weights', cmap_type='jet', figdim=(10, 10))

    # # 2) CURATION OF INTRA-HEMISPHERE CONNECTIVITY ON THE DCN CURATED SC
    # # 2.1 decide lobule-hemisphere ipsilateral and symmetrical connectivity
    idx_L = np.arange(96, 102+1, 1)
    idx_V = np.arange(106, 112+1, 1)
    #idx_V[0] = idx_V[0]+1  # trucchetto per avere 106 due volte. infatti arange parte da 105 --> la lascio lobulo-lobulo.
    # # 2.2 set Kp starting from SNN simulation (Geminiani et al., 2019)
    Kp = (907.9*70 + 1463*99 + 484.4*299 + 735.4*14) / (70 + 99 + 299 + 247) #media pesata per la numerosità di cellule
    # # 0.2 perchè ho sempre preso il 20%
    Kp = 0.2 * Kp

    # # 2.2.1 norm CRBL and * 1e-3
    #SC_curated_parallel = mapping_parallel(SC_curated, Kp*1e-3, np.array(lob_vols_mm), np.array(CRBL_vols_mm), idx_L, idx_V, fromRtoL=23)

    # # 2.2.2 norm ICV --> TENGO questo perchè così non ho valori casuali
    SC_curated_parallel = mapping_parallel(SC_curated, Kp, np.array(lob_vols_mm), np.array(ICV_mm), idx_L, idx_V, fromRtoL=23)

    save_curated_matrix(SC_curated_parallel, SC_path_DCN, SUB_DIR, conn_folder2)

    #plot_your_matrix(SC_curated_parallel, labels, 3, title='SC', cbar_name='weights', cmap_type='jet', figdim=(10, 10))

    if args.plot_mat:
    #check all brain
        plot_2_matrices(matrix=SC_curated_parallel, labels=labels, step_labels=3,
                title='Whole-brain CURATED SC', cbar_name='weigths', cmap='jet',
                matrix1=SC_subj, labels1=labels, step_labels1=3,
                title1='Whole-brain SC', cbar_name1='weigths', cmap1='jet',
                figdim=(16, 8))
    #check cerebellum
        plot_2_matrices(matrix=SC_curated_parallel[93:,93:], labels=labels[93:], step_labels=1,
                title='Cerebellar CURATED SC', cbar_name='weigths', cmap='jet',
                matrix1=SC_subj[93:,93:], labels1=labels[93:], step_labels1=1,
                title1='Cerebellar SC', cbar_name1='weigths', cmap1='jet',
                figdim=(16, 8))
if __name__ == "__main__":
    main()

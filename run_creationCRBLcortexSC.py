from tools_for_SCsubnetworks import *
from tools_for_curation_SC import *

if __name__ == '__main__':
    import argparse
    import numpy as np
    import zipfile
    import os
    import matplotlib.pyplot as plt

    parser = argparse.ArgumentParser(description=
                                     """ 
                                   Main routine to create a subnetwork from SC matrix.
                                   Here used to create the cerebellar subnetwork from AAL-SUIT Atlas
                                   """,
                                     formatter_class=argparse.RawTextHelpFormatter)


    parser.add_argument('SUB_ID',
                        type=str,
                        help="Subject ID")

    parser.add_argument('--prot_dir',
                        type=str,
                        default='/Users/robertalorenzi/Documents/4_Postdoc/0ngoing/1_MF/1_MF_Integration/Data/connectivity_data/HCP_TVBmm_30M/',
                        help="protocol_directory")

    parser.add_argument('--suffix_subSC',
                        type=str,
                        default='_ONLYCRBL',
                        help="suffix for the subnetwork in txt and zip. E.g.: <name>_<suffix_subSC>.zip")

    parser.add_argument('--conn_zipname',
                        type=str,
                        default='SC_dirCB.zip',
                        help="zip directory for TVB simulation")

    parser.add_argument('--conn_dir',
                        type=str,
                        default='Connectome_all',
                        help="name of the connectome directory")

    parser.add_argument('--subnet_ind',
                        type=int,
                        default=np.array([93, -1]),
                        help="first and last index of the subnetwork. Default for the cerebellum from AAL_SUIT 23 centers atlas (Fastigial included)")

    parser.add_argument('--DCN_idx',
                        type=int,
                        default=np.array([103, 104, 105, 113, 114, 115]),
                        help="Deep cerebellar nuclei Index. Default from AAL_SUIT 32 centers atlas (Fastigial included)")

    parser.add_argument('--new_val',
                        type=float,
                        default=-1.,
                        help="default value to create the mask for DCN")


    args = parser.parse_args()
    SUB_ID = args.SUB_ID

    prot_folder = args.prot_dir
    conn_folder = args.conn_dir

    zip_dirname = args.conn_zipname

    DCN_idx = args.DCN_idx
    first_ind = args.subnet_ind[0]
    last_ind = args.subnet_ind[-1]

    suffix_subSC = args.suffix_subSC

    # STARTING OPERATIONS ----------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    SUB_DIR = prot_folder + SUB_ID

    # name just to call txt of the subnetwork with the big network name ------------------------------------------------
    SC_path_w = 'atlas_SC_count_dirCb_NORM_CURATED.txt'
    SC_path_t = 'atlas_SC_length_dirCb.txt'

    # Reading from ZIP Archive built for tvb ---------------------------------------------------------------------------
    FOLDER = SUB_DIR + zip_dirname

    # Extract txt from zip folder
    txt_path_w = extract_txt(FOLDER, name_txt='weights.txt')
    txt_path_tl = extract_txt(FOLDER, name_txt='tract_lengths.txt')
    txt_path_c = extract_txt(FOLDER, name_txt='centres.txt')

    # Read from extracted location
    weights = read_txt(txt_path_w)
    tracts = read_txt(txt_path_tl)
    centres = read_centre_txt(txt_path_c)

    # Remove_DCN -------------------------------------------------------------------------------------------------------
    weights_no_DCN, tracts_no_DCN, centers_no_DCN = delete_DCN(weights, tracts, centres, DCN_idx)

    # Extract CRBL CORTEX subnetwork -----------------------------------------------------------------------------------
    subnetwork_weights = weights_no_DCN[first_ind:last_ind, first_ind:last_ind]
    subnetwork_tracts = tracts_no_DCN[first_ind:last_ind, first_ind:last_ind]
    subnetwork_centres = centers_no_DCN[first_ind:last_ind]

    # Saving the subnetwork --------------------------------------------------------------------------------------------
    w_sub_filename = save_curated_matrix(subnetwork_weights, SC_path_w, SUB_DIR, conn_folder, suffix_subSC)
    t_sub_filename = save_curated_matrix(subnetwork_tracts, SC_path_t, SUB_DIR, conn_folder, suffix_subSC)

    save_txt_centres(prot_folder+'centres_crbl_cortex.txt', subnetwork_centres)

    #Checking...
    #print('Shapes: ', np.shape(subnetwork_tracts), np.shape(subnetwork_weights))
    #plot_subnetworks(subnetwork_weights, subnetwork_tracts, subnetwork_weights)

    # Creating a zip archive for TVB -----------------------------------------------------------------------------------
    base_name = os.path.splitext(os.path.basename(args.conn_zipname))[0]
    name_mat4TVB_folder = base_name + suffix_subSC

    destination_dir = os.path.join(args.prot_dir, args.SUB_ID, name_mat4TVB_folder)

    try:
        os.makedirs(destination_dir, exist_ok=False)
        print("Directory '%s' created successfully" % destination_dir)
    except OSError as error:
        print("Directory '%s' already created!!!!"  % destination_dir)

    _, filename_w = os.path.split(w_sub_filename) #to get the filename
    _, filename_t = os.path.split(t_sub_filename) #to get the filename

    filenames = [filename_w, filename_t]

    built_zip_forTVB(SUB_DIR + conn_folder, destination_dir, filenames, prot_folder+'centres_crbl_cortex.txt')

from tools_for_SCsubnetworks import *

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


    parser.add_argument('FOLDER',
                        type=str,
                        default='/home/bcc/projects/IntegrationMFCRBL/Mouse/tvb_model_reference/data/Mouse_512/100307_Conn_Count_dirCRBL_masked.zip',
                        help="path of connectivity.zip")

    parser.add_argument('subnet_ind',
                        type=int,
                        default=np.array([93, 126]),
                        help="first and last index of the subnetwork. Default for the cerebellum from AAL_SUIT 23 centers atlas (Fastigial included)")

    parser.add_argument('-DCN_ind',
                        type=int,
                        default=np.array([103, 104, 105, 113, 114, 115]),
                        help="Deep cerebellar nuclei Index. Default from AAL_SUIT 32 centers atlas (Fastigial included)")

    parser.add_argument('--new_val',
                        type=float,
                        default=-1.,
                        help="default value to create the mask for DCN")


    args = parser.parse_args()

    first_ind = args.subnet_ind[0]
    last_ind = args.subnet_ind[-1]


    #Extract the weights from zip folder
    txt_path_w = extract_txt(args.FOLDER, name_txt = 'weights.txt')
    txt_path_tl = extract_txt(args.FOLDER, name_txt = 'tract_lengths.txt')
    txt_path_fc = extract_txt(args.FOLDER, name_txt = 'functZ.txt')

    #Read the weights from extracted location
    input_weights = read_txt(txt_path_w)
    input_tracts = read_txt(txt_path_tl)
    input_fc = read_txt(txt_path_fc)


    #Extract subnetwork
    subnetwork_weights = input_weights[first_ind:last_ind, first_ind:last_ind]
    subnetwork_tracts = input_tracts[first_ind:last_ind, first_ind:last_ind]
    subnetwork_fc = input_fc[first_ind:last_ind, first_ind:last_ind]

    print(np.shape(subnetwork_weights))
    print(np.shape(subnetwork_tracts))
    print(np.shape(subnetwork_fc))

    save_txt_matrix(mat_name=np.matrix(subnetwork_weights), txt_name='weights.txt', folder_name='100307_Conn_Count_dirCRBL_masked_ONLYCRBLnew')
    save_txt_matrix(mat_name=np.matrix(subnetwork_tracts), txt_name='tract_lengths.txt', folder_name='100307_Conn_Count_dirCRBL_masked_ONLYCRBLnew')
    save_txt_matrix(mat_name=np.matrix(subnetwork_fc), txt_name='functZ.txt', folder_name='100307_Conn_Count_dirCRBL_masked_ONLYCRBLnew')

    plot_subnetworks(subnetwork_weights, subnetwork_tracts, subnetwork_fc)

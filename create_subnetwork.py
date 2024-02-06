from tvb_preproc_tools import *

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


    parser.add_argument('-FOLDER',
                        type=str,
                        default='/Users/robertalorenzi/PycharmProjects/IntegrationMFCRBL/Mouse/tvb_model_reference/data/Mouse_512/Conn_Count_dirCRBL_100307_masked.zip',
                        help="path of connectivity.zip")

    parser.add_argument('-new_val',
                        type=float,
                        default=-1.,
                        help="default value to create the mask")


    args = parser.parse_args()


    #Extract the weights from zip folder
    txt_path_w = extract_weights(args.FOLDER)
    txt_path_tl = extract_tracts(args.FOLDER)

    #Read the weights from extracted location
    input_weights = read_weights(txt_path_w)
    input_tracts = read_weights(txt_path_w)

    #Extract subnetwork
    subnetwork_weights = input_weights[93:126, 93:126]
    subnetwork_tracts = input_tracts[93:126, 93:126]

    print(np.shape(subnetwork_weights))
    print(np.shape(subnetwork_tracts))

    save_txt_matrix(mat_name=np.matrix(subnetwork_weights), txt_name='weights.txt', folder_name='Conn_Count_dirCRBL_masked_ONLYCRBL')
    save_txt_matrix(mat_name=np.matrix(subnetwork_tracts), txt_name='tract_lengths.txt', folder_name='Conn_Count_dirCRBL_masked_ONLYCRBL')

    plot_weights_and_mask(subnetwork_weights, subnetwork_tracts, input_weights, input_tracts)

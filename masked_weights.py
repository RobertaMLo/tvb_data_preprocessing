from tvb_preproc_tools import *

if __name__ == '__main__':
    import argparse
    import numpy as np
    import zipfile
    import os
    import matplotlib.pyplot as plt

    parser = argparse.ArgumentParser(description=
                                     """ 
                                   Main routine to create a mask for SC matrix - weights.
                                   Used here to create a negative (inhibithory) connections FROM CRBL TO DCN
                                   """,
                                     formatter_class=argparse.RawTextHelpFormatter)


    parser.add_argument('-FOLDER',
                        type=str,
                        default='/Users/robertalorenzi/PycharmProjects/IntegrationMFCRBL/Mouse/tvb_model_reference/data/Mouse_512/Conn_Count_plusCRBL_100307.zip',
                        help="path of connectivity.zip")

    parser.add_argument('-new_val',
                        type=float,
                        default=-1.,
                        help="default value to create the mask")


    args = parser.parse_args()

    #Extract the weights from zip folder
    txt_path = extract_weights(args.FOLDER, 'weights.txt')

    #Read the weights from extracted location
    input_weights = read_weights(txt_path)

    #Define the indices of interest: for me now are from crbl to dcn
    from_crbl = np.arange(94, 126, 1)
    to_dcn = np.array([104, 105, 106, 114, 115, 116])

    #Create the mask - 1 and -1 --> -1 for inhibithory coupling
    crbl_dcn_mask = create_mask(input_weights, from_region=from_crbl, to_region=to_dcn, new_val=-1)

    #Compute new weights
    new_weights = input_weights*crbl_dcn_mask

    #Check
    print('INPUT WEIGHTS:\n', input_weights[104, 95])
    print('MASKED WEIGHTS:\n', new_weights[104, 95])

    plot_weights_and_mask(input_weights[94:, 94:], crbl_dcn_mask[94:, 94:], new_weights[94:, 94:])
    plot_weights_and_mask(input_weights, crbl_dcn_mask, new_weights, difference=input_weights-new_weights)

    np.savetxt('weights.txt', new_weights)






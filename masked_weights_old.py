
def extract_weights(zip_conn_folder):

    archive = zipfile.ZipFile(zip_conn_folder)
    for file in archive.namelist():
        #print(file)
        if 'weights.txt' in file:
            if '__MAC' not in file: #maybe if you don't have a mac this is unuseful
                archive.extract(file, os.getcwd())
                dir_name = file

    return os.getcwd() + '/' + dir_name


def read_weights(file_txt_path):
    input = np.loadtxt(file_txt_path, dtype='float', delimiter=' ')
    print(input)

    return input


def create_mask(weights, from_region, to_region, new_val):

    mask_w = np.ones(np.shape(weights))

    for tr in to_region:
        for fr in from_region:
            #print(fr)
            #print(tr)

            mask_w[tr, fr] = mask_w[tr, fr] * new_val
            print(mask_w[tr,fr])

    np.fill_diagonal(mask_w, 1)


    return mask_w

def plot_weights_and_mask(weights, mask, new_weights):

    interp = 'nearest' #'bilinear'
    fig, axs = plt.subplots(nrows=2, ncols=2, sharex=True, figsize=(7, 3))

    axs[0, 0].set_title('SC weights')
    pos0 = axs[0, 0].imshow(weights, cmap = 'jet', vmin=np.min(new_weights), vmax=np.max(weights), origin= 'upper', interpolation=interp)
    fig.colorbar(pos0, ax=axs[0, 0], anchor=(0, 0.3), shrink=0.7)

    axs[0, 1].set_title('SC masked weights')
    pos1 = axs[0, 1].imshow(new_weights, cmap = 'jet', vmin=np.min(new_weights), vmax=np.max(weights), origin='upper', interpolation=interp)
    fig.colorbar(pos1, ax=axs[0, 1], anchor=(0, 0.3), shrink=0.7)

    axs[1, 0].set_title('Mask')
    pos2 = axs[1, 0].imshow(mask, cmap = 'binary', origin='upper', interpolation=interp)
    fig.colorbar(pos2, ax=axs[1, 0], anchor=(0, 0.3), shrink=0.7)

    axs[1, 1].set_title('Difference')
    pos3 = axs[1, 1].imshow(weights-new_weights, cmap = 'RdPu', origin='upper', interpolation=interp)
    fig.colorbar(pos3, ax=axs[1, 1], anchor=(0, 0.3), shrink=0.7)

    plt.show()



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
    txt_path = extract_weights(args.FOLDER)

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
    plot_weights_and_mask(input_weights, crbl_dcn_mask, new_weights)

    np.savetxt('weights.txt', new_weights)






import numpy as np
import zipfile
import os
import matplotlib.pyplot as plt

def extract_txt(zip_conn_folder, name_txt):

    archive = zipfile.ZipFile(zip_conn_folder)
    for file in archive.namelist():
        #print(file)
        if name_txt in file:
            if '__MAC' not in file: #maybe if you don't have a mac this is unuseful
                archive.extract(file, os.getcwd())
                dir_name = file

    return os.getcwd() + '/' + dir_name


def read_txt(file_txt_path):
    input = np.loadtxt(file_txt_path, dtype='float', delimiter=' ')
    print(input)

    return input


def read_centre_txt(file_centre_path):
    """
    Function to read centre.txt which is a txt file with both lables (string) and centres (float)
    :param file_centre_path: full path of the centre file
    :return: dcitionary containing labels and MNI centers
    """
    # Read the contents of the file
    with open(file_centre_path, "r") as file:
        lines = file.readlines()

    return lines


def create_mask(weights, from_region, to_region, new_val):

    mask_w = np.ones(np.shape(weights))

    for tr in to_region:
        for fr in from_region:
            #print(fr)
            #print(tr)

            mask_w[tr, fr] = mask_w[tr, fr] * new_val
            print(mask_w[tr, fr])

    np.fill_diagonal(mask_w, 1)
    return mask_w


def delete_DCN(weights, tracts, centers, DCN_idx):

    mask = np.ones(np.shape(weights)[0], dtype=bool)
    mask[DCN_idx] = False

    weights_no_DCN = weights[mask, :]
    weights_no_DCN = weights_no_DCN[:, mask]

    tracts_no_DCN = tracts[mask, :]
    tracts_no_DCN = tracts_no_DCN[:, mask]

    centers_no_DCN = [centres for i, centres in enumerate(centers) if i+1 not in DCN_idx]

    return weights_no_DCN, tracts_no_DCN, centers_no_DCN


def save_txt_centres(file_path, centres):

    with open(file_path, "w") as file:
        file.writelines(centres)


def plot_weights_and_mask(weights, mask, new_weights, difference):

    interp = 'nearest' #'bilinear'
    fig, axs = plt.subplots(nrows=2, ncols=2, sharex=True, figsize=(7, 3))

    axs[0, 0].set_title('SC weights')
    pos0 = axs[0, 0].imshow(weights, cmap = 'jet', vmin=np.min(new_weights), vmax=np.max(weights), origin= 'upper', interpolation=interp)
    fig.colorbar(pos0, ax=axs[0, 0], anchor=(0, 0.3), shrink=0.7)

    axs[0, 1].set_title('SC masked weights')
    pos1 = axs[0, 1].imshow(new_weights, cmap = 'jet', vmin=np.min(new_weights), vmax=np.max(weights), origin='upper', interpolation=interp)
    fig.colorbar(pos1, ax=axs[0, 1], shrink=0.7)

    axs[1, 0].set_title('Mask')
    pos2 = axs[1, 0].imshow(mask, cmap = 'binary', origin='upper', interpolation=interp)
    fig.colorbar(pos2, ax=axs[1, 0], shrink=0.7)

    axs[1, 1].set_title('Difference')
    pos3 = axs[1, 1].imshow(difference, cmap = 'RdPu', origin='upper', interpolation=interp)
    fig.colorbar(pos3, ax=axs[1, 1], shrink=0.7)

    plt.show()


def plot_subnetworks(weights, tracts, fc):

    interp = 'nearest' #'bilinear'
    fig, axs = plt.subplots(nrows=1, ncols=3, sharex=True, figsize=(15, 3))

    axs[0].set_title('SC weights')
    pos0 = axs[0].imshow(weights, cmap = 'jet', vmin=np.min(weights), vmax=np.max(weights), origin= 'upper', interpolation=interp)
    fig.colorbar(pos0, ax=axs[0], anchor=(0, 0.3), shrink=0.7)

    axs[1].set_title('SC tract lengths')
    pos1 = axs[1].imshow(tracts, cmap = 'jet', vmin=np.min(tracts), vmax=np.max(tracts), origin='upper', interpolation=interp)
    fig.colorbar(pos1, ax=axs[1], anchor=(0, 0.3), shrink=0.7)

    axs[2].set_title('FC')
    pos2 = axs[2].imshow(fc, cmap = 'RdBu_r', origin='upper', interpolation=interp)
    fig.colorbar(pos2, ax=axs[2], anchor=(0, 0.3), shrink=0.7)

    plt.show()




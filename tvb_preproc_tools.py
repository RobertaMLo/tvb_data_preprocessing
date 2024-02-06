import argparse
import numpy as np
import zipfile
import os
import matplotlib.pyplot as plt


def extract_weights(zip_conn_folder):

    archive = zipfile.ZipFile(zip_conn_folder)
    for file in archive.namelist():
        #print(file)
        if 'weights.txt' in file:
            if '__MAC' not in file: #maybe if you don't have a mac this is unuseful
                archive.extract(file, os.getcwd())
                dir_name = file

    return os.getcwd() + '/' + dir_name


def extract_tracts(zip_conn_folder):

    archive = zipfile.ZipFile(zip_conn_folder)
    for file in archive.namelist():
        #print(file)
        if 'tract_lengths.txt' in file:
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

def save_txt_matrix(mat_name, txt_name, folder_name):

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    txt_full_path = os.getcwd()+'/'+folder_name+'/'+txt_name

    with open(txt_full_path, 'w') as f:
        for line in mat_name:
            np.savetxt(f, line)

    print('saved: ', folder_name + '/' + txt_name)

def plot_weights_and_mask(weights, mask, new_weights, difference):

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
    pos3 = axs[1, 1].imshow(difference, cmap = 'RdPu', origin='upper', interpolation=interp)
    fig.colorbar(pos3, ax=axs[1, 1], anchor=(0, 0.3), shrink=0.7)

    plt.show()





import numpy as np
import os
import shutil
import zipfile

def merge_SC_all_radial(SCall, SCrad, idxdent):

    SCnew = np.ones_like(SCall) * SCall

    #cerebrum-cerebellar cortex con curation
    SCnew[:93, :93] = np.ones_like(SCall[:93, :93])*SCrad[:93, :93]

    #Elimino le connessioni intracerebellari TUTTE
    SCnew[93:, 93:] = 0

    #Ri-Aggiungo le connessioni con DENTATI
    SCnew[idxdent, :] = SCall[idxdent, :]
    SCnew[:, idxdent] = SCall[:, idxdent]
    #Le connessioni con le parallel e il feedback da dentati non è apprezzabile da MRI quindi non in questa funzione.
    #Vedi funzioni sotto!

    return SCnew

def fix_fromdentate2crblctx(SC, dent_index):

    SCdent = np.ones_like(SC)*SC
    new_val = np.array(0.1 * SC[dent_index, :])

    # Create a mask for dent_index
    mask = np.zeros(SC.shape[0], dtype=bool)
    mask[dent_index] = True

    # Broadcast
    SCdent[:, mask] = new_val.T
    return SCdent

def mapping_parallel_frog(SC, idx_parallel=[]):
    print('VALID ONLY FOR 100307 HCP!!!!')
    SC_parallel_map = SC * 0
    #From Vermis 2 Right Lobes
    SC_parallel_map[95, 106] = 0.04478
    SC_parallel_map[96, 107] = 0.05759
    SC_parallel_map[96, 108] = 0.05662
    SC_parallel_map[97, 108] = 0.045
    SC_parallel_map[97, 109] = 0.0487787
    SC_parallel_map[97, 110] = 0.0465596
    SC_parallel_map[97, 111] = 0.0465952

    SC_parallel_map[98, 107] = 0.0214305
    SC_parallel_map[98, 108] = 0.0204561

    SC_parallel_map[99, 107] = 0.0193465
    SC_parallel_map[99, 108] = 0.0183720
    SC_parallel_map[99, 109] = 0.0221489

    SC_parallel_map[100, 109] = 0.0180449
    SC_parallel_map[100, 110] = 0.0158257
    SC_parallel_map[100, 111] = 0.0158257

    SC_parallel_map[101, 111] = 0.0129949
    SC_parallel_map[101, 112] = 0.0116577

    SC_parallel_map[102, 112] = 0.0034069

    #From Right Lobes 2 Vermis
    # As above

    #From Vermis 2 Left Lobes
    fromRtoL = 23 # how many nodes to get the correspondant opposit

    SC_parallel_map[95 + 23, 106] = 0.0437999
    SC_parallel_map[96 + 23, 107] = 0.0604862
    SC_parallel_map[96 + 23, 108] = 0.0595118
    SC_parallel_map[97 + 23, 108] = 0.045
    SC_parallel_map[97 + 23, 109] = 0.04400613
    SC_parallel_map[97 + 23, 110] = 0.0417870
    SC_parallel_map[97 + 23, 111] = 0.0418225

    SC_parallel_map[98 + 23, 107] = 0.0229028
    SC_parallel_map[98 + 23, 108] = 0.0219284

    SC_parallel_map[99 + 23, 107] = 0.0206197
    SC_parallel_map[99 + 23, 108] = 0.0196452
    SC_parallel_map[99 + 23, 109] = 0.0234220

    SC_parallel_map[100 + 23, 109] = 0.0194461
    SC_parallel_map[100 + 23, 110] = 0.0172269
    SC_parallel_map[100 + 23, 111] = 0.0172625

    SC_parallel_map[101 + 23, 111] = 0.0140618
    SC_parallel_map[101 + 23, 112] = 0.0127246

    SC_parallel_map[102 + 23, 112] = 0.0031438

    # From Left Lobes 2 Vermis
    # As above

    # To get symmetric, sum with the transpose
    SC_parallel_map_transpose = SC_parallel_map.T
    SC_parallel_map = SC_parallel_map + SC_parallel_map_transpose

    return SC_parallel_map


def mapping_parallel(SC, Kp, Lob_vols, ICV, idx_L, idx_V, fromRtoL=23):

    SC_parallel_map = np.ones_like(SC)*SC
    idx_R = idx_L + fromRtoL

    # TO Left Hemisphere FROM Vermis
    SC_parallel_map[idx_L, idx_V] = Kp * (np.mean(np.array([Lob_vols[idx_L-93], Lob_vols[idx_V-93]]), axis=0)/ICV)

    # TO Rigth Hemisphere FROM Vermis
    SC_parallel_map[idx_R, idx_V] = Kp * (np.mean(np.array([Lob_vols[idx_R-93], Lob_vols[idx_V-93]]), axis=0)/ICV)

    # TO Vermis from Hemispheres R and L
    # for the moment matrix is symmetric
    SC_parallel_map[idx_V, idx_L] = Kp * (np.mean(np.array([Lob_vols[idx_L - 93], Lob_vols[idx_V - 93]]), axis=0) / ICV)
    SC_parallel_map[idx_V, idx_R] = Kp * (np.mean(np.array([Lob_vols[idx_R - 93], Lob_vols[idx_V - 93]]), axis=0) / ICV)

    return SC_parallel_map


def read_txt_vol(filename):
    with open(filename, 'r') as file:
        # Initialize lists to store data from each column
        vol_vox = []
        vol_mm = []

        # Read each line in the file
        for line in file:
            # Split the line into elements
            elements = line.split()
            # Store data into respective columns
            vol_vox.append(float(elements[0]))
            vol_mm.append(float(elements[1]))

    return vol_vox, vol_mm


def save_curated_matrix(matrix_to_save, original_filename, SUB_DIR, conn_folder, name_suffix="_CURATED"):

    # Extract the base name of the file (without extension). Pos 0 = filename, Pos 1 = extension
    base_name = os.path.splitext(os.path.basename(original_filename))[0]

    # Save the matrix to a new file with the desired name pattern
    curated_filename = os.path.join(SUB_DIR, conn_folder, base_name + name_suffix + ".txt")
    print('ehiiiii', curated_filename)

    np.savetxt(curated_filename, matrix_to_save)
    print(curated_filename + ' successfully saved')
    return curated_filename


def built_zip_forTVB(subject_folder, dest_dir, filenames, centres_filepath):

    # mapping of filename into name specific for TVB
    filename_mapping = {
        filenames[0]: 'weights.txt',
        filenames[1]: 'tract_lengths.txt',
    }

    #Check if file exists
    for filename in filenames:
        file_path = os.path.join(subject_folder, filename)
        if os.path.exists(file_path):
            #updating filenames
            dest_filename = filename_mapping.get(filename, filename)
            #copying file with updated filenames
            shutil.copy(file_path, os.path.join(dest_dir, dest_filename))

    #copying centres file
    _, c_filename = os.path.split(centres_filepath)
    shutil.copy(centres_filepath, os.path.join(dest_dir, 'centres.txt'))

    # Zip the destination directory
    shutil.make_archive(dest_dir, 'zip', dest_dir)


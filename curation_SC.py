import numpy as np

def merge_SC_DTIapproach(SCcur, SCstd, idxdent):

    SCnew = np.ones_like(SCcur)*SCcur

    #cerebrum-cerebellar cortex con curation
    SCnew[:93, :93] = SCstd[:93, :93]

    #Elimino le connessioni intracerebellari TUTTE
    SCnew[93:, 93:] = 0

    #Ri-Aggiungo le connessioni con DENTATI
    SCnew[idxdent, :] = SCcur[idxdent, :]
    SCnew[:, idxdent] = SCcur[:, idxdent]
    #Le connessioni con le parallel e il feedback da dentati non è apprezzabile da MRI quindi non in questa funzione.
    #Vedi funzioni sotto!

    return SCnew

def fix_from_dentate2crblctx(SC, dent_index):

    SCdent = np.ones_like(SC)*SC
    new_val = np.array(0.1 * SC[dent_index, :])

    # Create a mask for dent_index
    mask = np.zeros(SC.shape[0], dtype=bool)
    mask[dent_index] = True

    # Broadcast
    SCdent[:, mask] = new_val.T
    return SCdent

def mapping_parallel(SC, idx_parallel=[]):

    SC_parallel_map = SC * 0
    #From Vermis 2 Right Lobes
    SC_parallel_map[95, 106] = 1
    SC_parallel_map[96, 107:109] = 1
    SC_parallel_map[97, 108:112] = 1
    SC_parallel_map[98, 107:109] = 1
    SC_parallel_map[99, 107:110] = 1
    SC_parallel_map[100, 109:112] = 1
    SC_parallel_map[101, 111:113] = 1
    SC_parallel_map[102, 112] = 1

    #From Right Lobes 2 Vermis
    # As above

    #From Vermis 2 Left Lobes
    fromRtoL = 23 # how many nodes to get the correspondant opposit

    SC_parallel_map[95 + fromRtoL, 106] = 1
    SC_parallel_map[96 + fromRtoL, 107:109] = 1
    SC_parallel_map[97 + fromRtoL, 108:112] = 1
    SC_parallel_map[98 + fromRtoL, 107:109] = 1
    SC_parallel_map[99 + fromRtoL, 107:110] = 1
    SC_parallel_map[100 + fromRtoL, 109:112] = 1
    SC_parallel_map[101 + fromRtoL, 111:113] = 1
    SC_parallel_map[102 + fromRtoL, 112] = 1

    # From Left Lobes 2 Vermis
    # As above

    # To get symmetric, sum with the transpose
    SC_parallel_map_transpose = SC_parallel_map.T
    SC_parallel_map = SC_parallel_map + SC_parallel_map_transpose

    return SC_parallel_map

def compute_parallel(SC_map, Kp):
    return SC_map*Kp





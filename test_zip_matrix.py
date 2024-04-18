from tools_for_curation_SC import built_zip_forTVB
import os

#root_path = '/Users/robertalorenzi/Documents/4_Postdoc/0ngoing/1_MF/1_MF_Integration/Data/connectivity_data/'
root_path = '/media/bcc/Volume/Analysis/Roberta/'

prot_folder = 'HCP_TVBmm_30M/'
#prot_folder = 'HCP_TVBmm/'
source_dir = os.path.join(root_path, prot_folder)

#subject_ids = ['100307/T1w', '101915/T1w', '103414/T1w']
subject_ids = ['103414/T1w', '103818/T1w', '108828/T1w', '110411/T1w', '111312/T1w', '111716/T1w']
conn_folder = 'Connectome_all'
#conn_folder = 'Connectome'

#centres_filepath = root_path + 'centres_crbl_cortex.txt'
centres_filepath = '/home/bcc/matlab/Atlases/Parcellation/4TVB_centres32_brain_MNI_onlycrblctx.txt'

#name_mat4TVB_folder = 'SC_dirCB'
name_mat4TVB_folder = 'SC_dirCB_ONLYCRBL'

filenames = ['atlas_SC_count_dirCb_NORM_CURATED_ONLYCRBL.txt', 'atlas_SC_length_dirCb_ONLYCRBL.txt']
#filenames = ['atlas_SC_count_dirCb_NORM_CURATED.txt', 'atlas_SC_length_dirCb.txt']

for subject_id in subject_ids:

    subject_folder = os.path.join(source_dir, subject_id, conn_folder)

    if not os.path.exists(subject_folder):
        print(f"Subject folder for subject {subject_id} doesn't exist.")
        continue

    destination_dir = os.path.join(source_dir, subject_id, name_mat4TVB_folder)
    os.makedirs(destination_dir, exist_ok=True)

    built_zip_forTVB(subject_folder, destination_dir, filenames, centres_filepath)

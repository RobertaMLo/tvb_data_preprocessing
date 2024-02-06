"""
Script per capire come fa la ref a settare il param is_cortical dentro al modello
ref: https://github.com/the-virtual-brain/tvb-multiscale/blob/rising-net/examples/tvb_nest/notebooks/cerebellum/working_files/CerebWilsonCowanTVBonly_Griffiths.ipynb
cella 4
"""

import numpy as np
    ##### PARTE DEGLI INDICI #######
_inds = {}
### TO BE CHANGED - NOW I KNOW CRBL ARE THE LAST 33 NODES
    
_inds["crbl"]  = np.arange(93,126,1)
_inds["cortical"] = np.arange(0,93,1)
_inds["dcn"] = np.array([103, 104, 105, 113, 114, 115])
_region_label_mock = np.arange(1,127,1)
    

_inds["crbl"] = np.arange(len(_region_label_mock)).astype('i') #metto al posto di inds crbl un  vettore di interi lungo quando argomento di arange (
#print("inds after astype\n",inds)
_inds["crbl"] = np.delete(_inds["crbl"], _inds["cortical"]) #delete inds cortical(second input) from inds crbl(first input)
#print("inds afeter delete\n", inds)
_is_cortical = np.array([False] * _region_label_mock.shape[0]).astype("bool") #inizializzo a false
#print('shape 0 di region_labels:',region_label_mock.shape[0])
#print('Iscortical:\n', is_cortical)
_is_cortical[_inds["cortical"]] = True
_is_cortical[_inds["dcn"]] = True
#print('Final Iscortical:\n', _is_cortical)
_is_crbl = np.logical_not(_is_cortical)
#print('Final crbl:\n', _is_crbl)

is_cortical = _is_cortical
is_crbl = _is_crbl

print(np.shape(is_cortical))
print(np.shape(is_crbl))
print("check dcn in cortical: ", is_cortical[103])
print("check dcn in crbl: ", is_crbl[103])

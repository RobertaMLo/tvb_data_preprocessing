"""
Script per capire come fa la ref a settare il param is_cortical dentro al modello
ref: https://github.com/the-virtual-brain/tvb-multiscale/blob/rising-net/examples/tvb_nest/notebooks/cerebellum/working_files/CerebWilsonCowanTVBonly_Griffiths.ipynb
cella 4
"""

import numpy as np
inds = {}

inds["crbl"]  = np.arange(94,127,1)
inds["cortical"] = np.arange(1,94,1)
print("Loaded innds dictionary\n", inds)

region_label_mock = np.arange(1,127,1)

inds["crbl"] = np.arange(len(region_label_mock)).astype('i') #metto al posto di inds crbl un  vettore di interi lungo quando argomento di arange (
print("inds after astype\n",inds)


inds["crbl"] = np.delete(inds["crbl"], inds["cortical"]) #delete inds cortical(second input) from inds crbl(first input)
print("inds afeter delete\n", inds)

is_cortical = np.array([False] * region_label_mock.shape[0]).astype("bool") #inizializzo a false
print('shape 0 di region_labels:',region_label_mock.shape[0])
print('Iscortical:\n', is_cortical)

is_cortical[inds["cortical"]] = True
print('Final Iscortical:\n', is_cortical)


derivative = np.zeros((5,126)) + np.random.random((5,126))
print('dimension of derivative ********', np.shape(derivative))

print('size di is cortical', np.shape(derivative[0, is_cortical]))
print('size di derivative totale', np.shape(derivative[0]))

d1 = np.random.random((126,1))
print('size d1', np.shape(d1))
print('size d1 is cortical', np.shape(d1[is_cortical]))





## mi sa che faccio tutta sta roba per avere matrice di indici
## Da capire perchè non mi toglie il primo elem.. se metto da 1 a 127 invece di len label, mi toglie il 94

###Prova indici
#a = np.array(inds["crbl"])
#print(a)
#b = np.array(np.where(a > 100, a*(-1), a))
#print(b)

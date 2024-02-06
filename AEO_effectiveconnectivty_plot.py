import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

## Class to center diverging matplotlib to 0. (I.E. Zero is White)
class MidpointNormalize(mpl.colors.Normalize):
    def __init__(self, vmin, vmax, midpoint=0, clip=False):
        self.midpoint = midpoint
        mpl.colors.Normalize.__init__(self, vmin, vmax, clip)

    def __call__(self, value, clip=None):
        normalized_min = max(0, 1 / 2 * (1 - abs((self.midpoint - self.vmin) / (self.midpoint - self.vmax))))
        normalized_max = min(1, 1 / 2 * (1 + abs((self.vmax - self.midpoint) / (self.midpoint - self.vmin))))
        normalized_mid = 0.5
        x, y = [self.vmin, self.midpoint, self.vmax], [normalized_min, normalized_mid, normalized_max]
        return np.ma.masked_array(np.interp(value, x, y))


def read_weights(file_txt_path):
    input = np.loadtxt(file_txt_path, dtype='float', delimiter='\t')
    print(input)

    return input


def plot_weights_and_mask(matAE, matAO, labels):

    norm = MidpointNormalize(vmin=np.min(matAO), vmax=np.max(matAE), midpoint=0)
    #cmap = 'RdBu_r'

    interp = 'nearest' #'bilinear'
    fig, axs = plt.subplots(nrows=1, ncols=2, sharex=True, figsize=(16, 6))

    axs[0].set_title('Action Execution', fontsize=14 )
    pos0 = axs[0].imshow(matAE, cmap = 'seismic', norm=norm, origin= 'upper', interpolation=interp)
    cb0 = fig.colorbar(pos0, ax=axs[0], anchor=(0, 0.3), shrink=0.7)
    cb0.set_label('Influence [Hz]', fontsize=12)

    axs[1].set_title('Action Observation', fontsize = 14)
    #(matAO, cmap = 'bwr', vmin=np.min(matAO), vmax=np.max(matAE), origin='upper', interpolation=interp)
    pos1 = axs[1].imshow(matAO, cmap = 'seismic', norm=norm, origin='upper', interpolation=interp)
    cb1 = fig.colorbar(pos1, ax=axs[1], anchor=(0, 0.3), shrink=0.7)
    cb1.set_label('Influence [Hz]', fontsize=12)

    for ax in axs:
        # ax.yaxis.grid(True)
        # ax.xaxis.grid(True)
        ax.set_xticks(np.arange(0, len(labels), 1), labels, fontsize=10, rotation=90)
        ax.set_yticks(np.arange(0, len(labels), 1), labels, fontsize=10)

    plt.show()

    plt.show()


if __name__ == '__main__':

    root_path = '/Users/robertalorenzi/Desktop/ISMRM2024/AEO'
    AE = 'BMA_AE.txt'
    AO = 'AO_BMA.txt'

    matAE = read_weights(root_path +'/' + AE)
    matAO = read_weights(root_path +'/' + AO)

    labels = ['M1 L', 'SMAPMC L', 'SPL L', 'CC L', 'CRBL R', 'V1 BIL']
    print(labels)

    plot_weights_and_mask(matAE, matAO, labels)

#colormap also 'bwr'



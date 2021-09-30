import matplotlib.pyplot as plt
import numpy as np

f = np.genfromtxt('/home/kyle/repos/iuvs-dust-single-scattering-albedo/data/msl-tau-880-h-sol3068.txt', delimiter=',', skip_header=8)

msl_ls = f[879:906, 2]
msl_tau = f[879:906, 3]

plt.scatter(msl_ls, msl_tau)
plt.savefig('/home/kyle/repos/iuvs-dust-single-scattering-albedo/figures/gale_crater.pdf')

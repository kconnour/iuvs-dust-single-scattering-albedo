import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.lines as lines
import numpy as np
from astropy.io import fits

# TODO: match Icarus fonts + line thicknesses (gulliver)
# TODO: 2 column legend?
# TODO: trim down the white space, particularly at the top
# TODO: Fix the IUVS section to just read in the answer

plt.rc('pdf', fonttype=42)  # ???
plt.rc('ps', fonttype=42)  # postscript
font_size = 8
plt.rc('font', size=font_size)
plt.rc('axes', titlesize=font_size)
plt.rc('axes', labelsize=font_size)
plt.rc('axes', titlepad=3)  # Set a little space around the title
plt.rc('xtick', labelsize=font_size)
plt.rc('ytick', labelsize=font_size)
plt.rc('legend', fontsize=font_size)
plt.rc('figure', titlesize=font_size)
plt.rc('font', **{'family': 'STIXGeneral'})  # Set the font to Stix
plt.rc('mathtext', fontset='stix')  # Set all LaTeX font to Stix
plt.rc('text', usetex=False)

# Set the thickness of plot borders
plthick = 0.4
plt.rc('lines', linewidth=0.8)
plt.rc('axes', linewidth=plthick)
plt.rc('xtick.major', width=plthick)
plt.rc('xtick.minor', width=plthick)
plt.rc('ytick.major', width=plthick)
plt.rc('ytick.minor', width=plthick)
plt.rc('pdf', compression=3)
plt.rcParams.update({'font.size': 8})

fig, ax = plt.subplots()

# Set color
cividis = plt.get_cmap('cividis')
color_14 = list(cividis(0.1))
color_16 = list(cividis(0.35))
color_18 = list(cividis(0.6))
color_20 = list(cividis(0.85))

# Add IUVS results
iteration = 5
f0 = np.load(f'/home/kyle/ssa_retrievals/iteration{iteration}/new-fsp_new-pf_hapke-wolff_1-4size.npy')
g0 = np.load(f'/home/kyle/ssa_retrievals/iteration{iteration}/new-fsp_new-pf_hapke-wolff_1-6size.npy')
h0 = np.load(f'/home/kyle/ssa_retrievals/iteration{iteration}/new-fsp_new-pf_hapke-wolff_1-8size.npy')
i0 = np.load(f'/home/kyle/ssa_retrievals/iteration{iteration}/new-fsp_new-pf_hapke-wolff_2-0size.npy')

iteration: int = 6

# Load the retrieval
wavs = np.load('/home/kyle/iuvs_wavelengths.npy')
f = np.load(f'/home/kyle/ssa_retrievals/iteration{iteration}/new-fsp_new-pf_hapke-wolff_1-4size.npy')
g = np.load(f'/home/kyle/ssa_retrievals/iteration{iteration}/new-fsp_new-pf_hapke-wolff_1-6size.npy')
h = np.load(f'/home/kyle/ssa_retrievals/iteration{iteration}/new-fsp_new-pf_hapke-wolff_1-8size.npy')
i = np.load(f'/home/kyle/ssa_retrievals/iteration{iteration}/new-fsp_new-pf_hapke-wolff_2-0size.npy')

#f_high_unc = np.load('/home/kyle/ssa_retrievals/const-fsp_const-pf_hapke-wolff_1-5size_high-uncertainty.npy')
#f_low_unc = np.load('/home/kyle/ssa_retrievals/const-fsp_const-pf_hapke-wolff_1-5size_low-uncertainty.npy')
# Note regarding f: It has shape (6857, 19). 4774 of them are a NaN (they have
#  OD < 5 or too high SZA or EA. 2083 of them fit the OD and angular criteria

# Get the Gale crater pixel data
file = '/home/kyle/repos/pyuvs-rt/ssa_files/gale_pixels_slit.fits'
hdul = fits.open(file)

reflectance = hdul['reflectance'].data
uncertainty = hdul['uncertainty'].data

position = hdul['position'].data
szas = hdul['sza'].data
eas = hdul['ea'].data
ls = hdul['ls'].data

# Plot averages
inds = np.where((szas <= 50) & (eas <= 72) & (f[:, 0] >= 0))
f0 = np.mean(f0[inds], axis=0)
g0 = np.mean(g0[inds], axis=0)
h0 = np.mean(h0[inds], axis=0)
i0 = np.mean(i0[inds], axis=0)
f = np.mean(f[inds], axis=0)
g = np.mean(g[inds], axis=0)
h = np.mean(h[inds], axis=0)
i = np.mean(i[inds], axis=0)

# TODO: fix this in upcoming iteration
fnew = (f+f0)/2
gnew = (g+g0)/2
hnew = (h+h0)/2
inew = (i+i0)/2

ax.plot(wavs, fnew, color=color_14)
ax.plot(wavs, gnew, color=color_16)
ax.plot(wavs, hnew, color=color_18)
ax.plot(wavs, inew, color=color_20)
################ End garbage section

# Add MARCI results
ax.scatter([258, 320], [0.619, 0.648], color=color_16)
ax.scatter([258, 320], [0.625, 0.653], color=color_18)
ax.errorbar(258, 0.619, yerr=0.010, elinewidth=1, capthick=1, capsize=3, color=color_16, alpha=0.6)
ax.errorbar(320, 0.648, yerr=0.005, elinewidth=1, capthick=1, capsize=3, color=color_16, alpha=0.6)
ax.errorbar(258, 0.625, yerr=0.011, elinewidth=1, capthick=1, capsize=3, color=color_18, alpha=0.6)
ax.errorbar(320, 0.653, yerr=0.005, elinewidth=1, capthick=1, capsize=3, color=color_18, alpha=0.6)

# Add the legend
dust_14 = patches.Patch(color=color_14, label=r'1.4 $\mu$m dust')
dust_16 = patches.Patch(color=color_16, label='1.6 $\mu$m dust')
dust_18 = patches.Patch(color=color_18, label='1.8 $\mu$m dust')
dust_20 = patches.Patch(color=color_20, label='2.0 $\mu$m dust')

iuvs_symbol = lines.Line2D([], [], color='k', label='IUVS results')
marci_symbol = lines.Line2D([], [], color='k', label='MARCI results', marker='o', linewidth=0)
handles = [dust_14, dust_16, dust_18, dust_20, iuvs_symbol, marci_symbol]
ax.legend(handles=handles)

# Set ticks
ax.set_xticks(np.linspace(200, 325, num=6))
ax.set_xticks(np.linspace(200, 325, num=int((325-200)/5+1)), minor=True)
ax.set_yticks(np.linspace(0.6, 0.68, num=int((0.68-0.6)/0.005+1)), minor=True)

ax.set_xlim(200, 325)
ax.set_ylim(0.6, 0.68)
ax.set_xlabel('Wavelength (nm)')
ax.set_ylabel('Single scattering albedo')

plt.savefig(f'/home/kyle/repos/iuvs-dust-single-scattering-albedo/figures/ssa_spectra.png', dpi=300)

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.lines as lines
import numpy as np
from astropy.io import fits

# TODO: match Icarus fonts + line thicknesses (gulliver)
# TODO: 2 column legend?
# TODO: trim down the white space, particularly at the top
# TODO: Fix the IUVS section to just read in the answer


def setup_plot():
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


def make_cividis_colors():
    cividis = plt.get_cmap('cividis')
    return list(cividis(0.1)), list(cividis(0.35)), list(cividis(0.6)), \
        list(cividis(0.85))


if __name__ == '__main__':
    setup_plot()
    color_14, color_16, color_18, color_20 = make_cividis_colors()

    fig = plt.figure()
    crism_data = plt.axes([0.75, 0.75, 0.2, 0.2])
    whole = plt.axes([0, 0, 1, 1])
    whole.patch.set_alpha(0)
    iuvs_data = plt.axes([0.1, 0.1, 0.85, 0.6])
    iuvs_data.patch.set_alpha(0.85)

    #whole = fig.add_axes([0, 0, 1, 1])
    #iuvs_data = fig.add_axes([0.1, 0.1, 0.7, 0.7])
    #crism_data = fig.add_axes([0.85, 0.85, 0.1, 0.1])

    # Load IUVS results
    f = np.load(f'/home/kyle/ssa_retrievals/iteration8/new-fsp_new-pf_hapke-wolff_1-4size.npy')
    g = np.load(f'/home/kyle/ssa_retrievals/iteration8/new-fsp_new-pf_hapke-wolff_1-6size.npy')
    h = np.load(f'/home/kyle/ssa_retrievals/iteration8/new-fsp_new-pf_hapke-wolff_1-8size.npy')
    i = np.load(f'/home/kyle/ssa_retrievals/iteration8/new-fsp_new-pf_hapke-wolff_2-0size.npy')
    wavs = np.load('/home/kyle/iuvs_wavelengths.npy')

    f_hi = np.load(f'/home/kyle/ssa_retrievals/iteration8/new-fsp_new-pf_hapke-wolff_1-4size-highUnc.npy')
    f_lo = np.load(f'/home/kyle/ssa_retrievals/iteration8/new-fsp_new-pf_hapke-wolff_1-4size-lowUnc.npy')
    g_hi = np.load(f'/home/kyle/ssa_retrievals/iteration8/new-fsp_new-pf_hapke-wolff_1-6size-highUnc.npy')
    g_lo = np.load(f'/home/kyle/ssa_retrievals/iteration8/new-fsp_new-pf_hapke-wolff_1-6size-lowUnc.npy')
    h_hi = np.load(f'/home/kyle/ssa_retrievals/iteration8/new-fsp_new-pf_hapke-wolff_1-8size-highUnc.npy')
    h_lo = np.load(f'/home/kyle/ssa_retrievals/iteration8/new-fsp_new-pf_hapke-wolff_1-8size-lowUnc.npy')
    i_hi = np.load(f'/home/kyle/ssa_retrievals/iteration8/new-fsp_new-pf_hapke-wolff_2-0size-highUnc.npy')
    i_lo = np.load(f'/home/kyle/ssa_retrievals/iteration8/new-fsp_new-pf_hapke-wolff_2-0size-lowUnc.npy')

    # Get the Gale crater pixel data
    file = '/home/kyle/repos/pyuvs-rt/ssa_files/gale_pixels_slit.fits'
    hdul = fits.open(file)

    reflectance = hdul['reflectance'].data
    uncertainty = hdul['uncertainty'].data

    position = hdul['position'].data
    szas = hdul['sza'].data
    eas = hdul['ea'].data
    ls = hdul['ls'].data

    inds = np.where((szas <= 50) & (eas <= 72) & (f[:, 0] >= 0))
    n_pix = np.sum(np.where((szas <= 50) & (eas <= 72) & (f[:, 0] >= 0), 1, 0))

    f_hi = np.sqrt(np.sum((f_hi[inds] - f[inds]) ** 2, axis=0)) / n_pix
    f_lo = np.sqrt(np.sum((f[inds] - f_lo[inds]) ** 2, axis=0)) / n_pix
    g_hi = np.sqrt(np.sum((g_hi[inds] - g[inds]) ** 2, axis=0)) / n_pix
    g_lo = np.sqrt(np.sum((g[inds] - g_lo[inds]) ** 2, axis=0)) / n_pix
    h_hi = np.sqrt(np.sum((h_hi[inds] - h[inds]) ** 2, axis=0)) / n_pix
    h_lo = np.sqrt(np.sum((h[inds] - h_lo[inds]) ** 2, axis=0)) / n_pix
    i_hi = np.sqrt(np.sum((i_hi[inds] - i[inds]) ** 2, axis=0)) / n_pix
    i_lo = np.sqrt(np.sum((i[inds] - i_lo[inds]) ** 2, axis=0)) / n_pix

    # Get the average spectra
    f = np.mean(f[inds], axis=0)
    g = np.mean(g[inds], axis=0)
    h = np.mean(h[inds], axis=0)
    i = np.mean(i[inds], axis=0)

    # Plot the IUVS data
    iuvs_data.plot(wavs, f, color=color_14)
    iuvs_data.fill_between(wavs, f + f_hi, f - f_lo, color=color_14, alpha=0.5, linewidth=0)
    iuvs_data.plot(wavs, g, color=color_16)
    iuvs_data.fill_between(wavs, g + g_hi, g - g_lo, color=color_16, alpha=0.5, linewidth=0)
    iuvs_data.plot(wavs, h, color=color_18)
    iuvs_data.fill_between(wavs, h + h_hi, h - h_lo, color=color_18, alpha=0.5, linewidth=0)
    iuvs_data.plot(wavs, i, color=color_20)
    iuvs_data.fill_between(wavs, i + i_hi, i - i_lo, color=color_20, alpha=0.5, linewidth=0)

    # Add MARCI results
    iuvs_data.scatter([258, 320], [0.619, 0.648], color=color_16)
    iuvs_data.scatter([258, 320], [0.625, 0.653], color=color_18)
    iuvs_data.errorbar(258, 0.619, yerr=0.010, elinewidth=1, capthick=1,
                       capsize=3, color=color_16, alpha=0.6)
    iuvs_data.errorbar(320, 0.648, yerr=0.005, elinewidth=1, capthick=1,
                       capsize=3, color=color_16, alpha=0.6)
    iuvs_data.errorbar(258, 0.625, yerr=0.011, elinewidth=1, capthick=1,
                       capsize=3, color=color_18, alpha=0.6)
    iuvs_data.errorbar(320, 0.653, yerr=0.005, elinewidth=1, capthick=1,
                       capsize=3, color=color_18, alpha=0.6)

    # Add the legend
    dust_14 = patches.Patch(color=color_14, label=r'1.4 ' + u'\u03bc' + 'm dust')
    dust_16 = patches.Patch(color=color_16, label=r'1.6 ' + u'\u03bc' + 'm dust')
    dust_18 = patches.Patch(color=color_18, label=r'1.8 ' + u'\u03bc' + 'm dust')
    dust_20 = patches.Patch(color=color_20, label=r'2.0 ' + u'\u03bc' + 'm dust')

    iuvs_symbol = lines.Line2D([], [], color='k', label='IUVS results')
    marci_symbol = lines.Line2D([], [], color='k', label='MARCI results',
                                marker='o', linewidth=0)
    handles = [dust_14, dust_16, dust_18, dust_20, iuvs_symbol, marci_symbol]
    iuvs_data.legend(handles=handles)

    # Set ticks
    ymax = 0.66
    ymin= 0.6
    iuvs_data.set_xticks(np.linspace(200, 325, num=6))
    iuvs_data.set_xticks(np.linspace(200, 325, num=int((325 - 200) / 5 + 1)),minor=True)
    iuvs_data.set_yticks(np.linspace(ymin, ymax, num=int((ymax - ymin) / 0.005 + 1)), minor=True)

    iuvs_data.set_xlim(200, 325)
    iuvs_data.set_ylim(ymin, ymax)
    iuvs_data.set_xlabel('Wavelength (nm)')
    iuvs_data.set_ylabel('Single scattering albedo')

    # CRISM
    cwav = [500, 600, 700, 800, 900, 1000]
    cssa = [0.83, 0.94, 0.97, 0.968, 0.965, 0.962]

    crism_data.plot(wavs, f, color=color_14, linewidth=0.5)
    crism_data.plot(wavs, g, color=color_16, linewidth=0.5)
    crism_data.plot(wavs, h, color=color_18, linewidth=0.5)
    crism_data.plot(wavs, i, color=color_20, linewidth=0.5)

    crism_data.axvline(325, ymax=0.06/0.4, color='k', linewidth=0.5)
    crism_data.axhline(0.66, xmax=125/800, color='k', linewidth=0.5)

    crism_data.plot(cwav, cssa, color='k')

    crism_data.set_xlim(200, 1000)
    crism_data.set_ylim(0.6, 1)
    crism_data.set_xticks([200, 600, 1000])
    crism_data.set_xticks(np.linspace(200, 1000, num=9), minor=True)
    crism_data.xaxis.tick_top()
    crism_data.yaxis.set_label_position('right')
    crism_data.yaxis.tick_right()

    # Connector lines
    a = np.array([0.7, 0.95])
    b = np.array([0.1, 0.85])

    # crism, iuvs
    whole.plot([0.78125, 0.95], [0.78, 0.7], color='k', linewidth=0.5, linestyle='--')
    whole.plot([0.75, 0.1], [0.78, 0.7], color='k', linewidth=0.5,linestyle='--')
    whole.plot([0.75, 0.1], [0.75, 0.1], color='k', linewidth=0.5,linestyle='--')
    whole.plot([0.78125, 0.95], [0.75, 0.1], color='k', linewidth=0.5,linestyle='--')

    whole.set_xlim(0, 1)
    whole.set_ylim(0, 1)

    plt.savefig(f'/home/kyle/repos/iuvs-dust-single-scattering-albedo/figures/ssa_spectra.pdf')

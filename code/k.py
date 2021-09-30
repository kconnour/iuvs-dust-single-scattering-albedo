import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.lines as lines
import numpy as np


def set_rc_params():
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
    return list(cividis(0)), list(cividis(0.1)), list(cividis(0.35)), \
        list(cividis(0.6)), list(cividis(0.85))


if __name__ == '__main__':
    k = np.loadtxt('/home/kyle/ssa_retrievals/iteration8/k.csv', delimiter=',')
    color_12, color_14, color_16, color_18, color_20 = make_cividis_colors()

    set_rc_params()
    fig, ax = plt.subplots()
    ax.plot(k[:, 0], k[:, 1], color=color_14)
    ax.plot(k[:, 0], k[:, 2], color=color_16)
    ax.plot(k[:, 0], k[:, 3], color=color_18)
    ax.plot(k[:, 0], k[:, 4], color=color_20)

    ymax = 0.022
    ymin= 0.01
    ax.set_xticks(np.linspace(200, 325, num=6))
    ax.set_xticks(np.linspace(200, 325, num=int((325 - 200) / 5 + 1)),minor=True)
    ax.set_yticks(np.linspace(ymin, ymax, num=7))
    ax.set_yticks(np.linspace(ymin, ymax, num=int((ymax - ymin) / 0.005 + 1)), minor=True)

    ax.set_xlim(200, 325)
    ax.set_ylim(ymin, ymax)
    ax.set_xlabel('Wavelength (nm)')
    ax.set_ylabel('k')

    # Add the legend
    dust_14 = patches.Patch(color=color_14, label=r'1.4 ' + u'\u03bc' + 'm dust')
    dust_16 = patches.Patch(color=color_16, label=r'1.6 ' + u'\u03bc' + 'm dust')
    dust_18 = patches.Patch(color=color_18, label=r'1.8 ' + u'\u03bc' + 'm dust')
    dust_20 = patches.Patch(color=color_20, label=r'2.0 ' + u'\u03bc' + 'm dust')

    handles = [dust_14, dust_16, dust_18, dust_20]
    ax.legend(handles=handles, loc='upper left')

    plt.savefig('/home/kyle/repos/iuvs-dust-single-scattering-albedo/figures/k.pdf')

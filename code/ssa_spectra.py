import matplotlib.pyplot as plt

fig, ax = plt.subplots()

# Set color
cividis = plt.get_cmap('cividis')
color_14 = list(cividis(0.1))
color_16 = list(cividis(0.35))
color_18 = list(cividis(0.6))
color_20 = list(cividis(0.85))

# Add MARCI results
ax.scatter([258, 320], [0.619, 0.648], label='MARCI 1.6 microns', color=color_16)
ax.scatter([258, 320], [0.625, 0.653], label='MARCI 1.8 microns', color=color_18)
ax.errorbar(258, 0.619, yerr=0.010, capsize=3, color=color_16)
ax.errorbar(320, 0.648, yerr=0.005, capsize=3, color=color_16)
ax.errorbar(258, 0.625, yerr=0.011, capsize=3, color=color_18)
ax.errorbar(320, 0.653, yerr=0.005, capsize=3, color=color_18)


ax.set_xlim(200, 325)
ax.set_ylim(0.58, 0.68)
ax.set_xlabel('Wavelength (nm)')
ax.set_ylabel('Single scattering albedo')

plt.legend()
plt.savefig(f'/home/kyle/repos/iuvs-dust-single-scattering-albedo/figures/ssa_spectra.png', dpi=300)

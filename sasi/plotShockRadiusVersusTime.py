#!/usr/bin/env python3

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
plt.style.use('publication.sty')

import globalVariables as gv

### Beginning of user input ###

dataDirectory = gv.dataDirectory + 'sasi/'

# Set xlabel and ylabel
xLabel = r'$t\ \left[\mathrm{ms}\right]$'
yLabel = r'$\left<R_{\mathrm{sh}}\right>\ \left[\mathrm{km}\right]$'

figName = gv.paperDirectory + 'Figures/fig.shockRadiusVersusTime.pdf'

### End of user input ###

t, Rsh = np.loadtxt(dataDirectory + 'shockRadiusVersusTime.dat')

fig, ax = plt.subplots()
ax.grid()
ax.set_xlim(t  .min() - 1.0, t  .max() + 1.0)
ax.set_ylim(Rsh.min() - 1.0, Rsh.max() + 1.0)
ax.set_xlabel(xLabel, fontsize = 16)
ax.set_ylabel(yLabel, fontsize = 16)

ax.plot(t, Rsh, 'k')

plt.savefig(figName, dpi = 300)
print('\n  Saved {:}'.format(figName))
plt.show()

import os
os.system('rm -rf __pycache__')

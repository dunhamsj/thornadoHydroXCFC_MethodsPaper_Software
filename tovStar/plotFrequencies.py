#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
plt.style.use( 'publication.sty' )

import globalVariables as gv

freq_max = 8.5e3
power_scale = 1.0e10

fig, axs = plt.subplots(5, 1)
prop = {'size': 7}

# Frequencies from Font et al., (2002), PRD, 65, 8
F  = [2.701e3, 4.563e3, 6.352e3, 8.129e3]

dirSuffix = ['_11'                       , '_11_11'                      , '_nX0032'                     , '_nX0064'                     , '_nX0128'                   ]
ID        = ['StaticTOV_multiLevel'      , 'StaticTOV_multiLevel'        , 'StaticTOV_singleLevel'       , 'StaticTOV_singleLevel'       , 'StaticTOV_singleLevel'     ]
ls        = ['-'                         , '-'                           , '-'                           , '-'                           , '-'                         ]
lab       = ['Two-Level ' + r'($N_{K} = 80$)', 'Three-Level ' + r'($N_{K} = 58$)' , 'Single-Level ' + r'($N_{K} = 32$)' , 'Single-Level ' + r'($N_{K} = 64$)' , 'Single-Level ' + r'($N_{K} = 128$)']
for i in range(len(ID)):

    ax = axs[i]
    for f in F:
        ax.axvline(f, c = 'k', ls = '--')
    filename = gv.dataDirectory + 'tovStar/' \
                 + '{:}{:}_fft.dat' \
                   .format(ID[i], dirSuffix[i])
    
    freq, power = np.loadtxt(filename)
    ind = np.where(freq < freq_max)[0]
    power /= power_scale
    ax.plot(freq[ind], power[ind], ls[i], c = 'k')
    ax.text \
      ( 0.02, 0.75, \
        lab[i], transform = ax.transAxes, \
        size = 8, \
        bbox = dict( facecolor = 'white', \
                     edgecolor = 'black', \
                     boxstyle = 'round' ) )
    if (i < axs.shape[0]-1):
        ax.xaxis.set_ticklabels([])

axs[0].text(F[0] * (1.0 + 0.03), 10.5, r'$F$')
axs[0].text(F[1] * (1.0 + 0.03), 10.5, r'$H_{1}$')
axs[0].text(F[2] * (1.0 + 0.01), 10.5, r'$H_{2}$')
axs[0].text(F[3] * (1.0 + 0.01), 10.5, r'$H_{3}$')
fig.supxlabel(r'$f\ \left[\mathrm{Hz}\right]$')
fig.supylabel(r'$10^{10} \times \mathrm{FFT\ of}\ \bar{\rho}_{<1\,\mathrm{km}}\left(t\right)$')
plt.subplots_adjust(hspace = 0)

figName = gv.paperDirectory + 'Figures/fig.fft.pdf'
plt.savefig(figName, dpi=300)
#plt.show()
print('\n  Saved {:}'.format(figName))

import os
os.system('rm -rf __pycache__')

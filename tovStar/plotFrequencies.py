#!/usr/bin/env python3

from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

import globalVariables as gv

fig, axs = plt.subplots(2, 1)
prop = {'size': 8}

ax = axs[0]
dirSuffix = ['_11_11'                    , '_nX0032'                     , '_nX0128'                   ]
ID        = ['StaticTOV_multiLevel'      , 'StaticTOV_singleLevel'       , 'StaticTOV_singleLevel'     ]
ls        = ['-'                         , '-'                           , '-'                         ]
lab       = ['Multi ' + r'($N_{K} = 58$)', 'Single ' + r'($N_{K} = 32$)' , 'Single ' + r'($N_{K} = 128$)']
c = [0, 1, -1]
for i in range(len(ID)):

    filename = gv.dataDirectory + 'tovStar/' \
                 + '{:}{:}_CentralDensityVersusTime.dat' \
                   .format(ID[0], dirSuffix[0])
    
    ind = np.where(freq_pos < 8.5e3)[0]
    ax.plot(freq_pos[ind], power_pos[ind])

ax.legend(prop=prop)
ax.grid()
ax.xaxis.set_ticklabels([])

ax = axs[1]
dirSuffix = ['_11'                       , '_nX0064'                     , '_nX0128'                     ]
ID        = ['StaticTOV_multiLevel'      , 'StaticTOV_singleLevel'       , 'StaticTOV_singleLevel'       ]
ls        = ['-'                         , '-'                           , '-'                           ]
lab       = ['Multi ' + r'($N_{K} = 80$)', 'Single ' + r'($N_{K} = 64$)' , 'Single ' + r'($N_{K} = 128$)']
c = [0, 1, -1]
for i in range(len(ID)):

    filename = gv.dataDirectory + 'tovStar/' \
                 + '{:}{:}_CentralDensityVersusTime.dat' \
                   .format(ID[0], dirSuffix[0])
    
    ind = np.where(freq_pos < 8.5e3)[0]
    ax.plot(freq_pos[ind], power_pos[ind])

ax.legend(prop=prop)
ax.grid()

fig.supxlabel(r'$f\ \left[\mathrm{Hz}\right]$')
fig.supylabel(r'$P\ \left[\mathrm{g \, cm}^{-3}\right]$')
plt.subplots_adjust(hspace = 0)

figName = gv.paperDirectory + 'Figures/fig.fft.pdf'
plt.savefig(figName, dpi=300)
#plt.show()
print('\n  Saved {:}'.format(figName))

import os
os.system('rm -rf __pycache__')

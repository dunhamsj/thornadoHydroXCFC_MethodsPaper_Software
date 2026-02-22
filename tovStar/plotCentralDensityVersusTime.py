#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
plt.style.use( 'publication.sty' )

import globalVariables as gv

nN = '02'

from getDensityData import *

fig, axs = plt.subplots(2, 1)
prop = {'size': 8}

ax = axs[0]
dirSuffix = ['_11_11'                    , '_nX0032'                     , '_nX0128'                   ]
ID        = ['StaticTOV_multiLevel'      , 'StaticTOV_singleLevel'       , 'StaticTOV_singleLevel'     ]
ls        = ['-'                         , '-'                           , '-'                         ]
lab       = ['Multi ' + r'($N_{K} = 32$)', 'Single ' + r'($N_{K} = 32$)' , 'Single ' + r'($N_{K} = 128$)']
c = [0, 1, -1]
for i in range(len(ID)):

    filename = gv.dataDirectory + 'tovStar/' \
                 + '{:}{:}_CentralDensityVersusTime.dat' \
                   .format(ID[i], dirSuffix[i])
    t, rhoC = np.loadtxt(filename)

    ax.plot(t, 1.0e4 * (rhoC - rhoC[0]) / rhoC[0], ls[i], c = gv.color[c[i]], \
            label = lab[i])
ax.legend(prop=prop)
ax.grid()
ax.xaxis.set_ticklabels([])

ax = axs[1]
dirSuffix = ['_11'                       , '_nX0064'                     , '_nX0128'                     ]
ID        = ['StaticTOV_multiLevel'      , 'StaticTOV_singleLevel'       , 'StaticTOV_singleLevel'       ]
ls        = ['-'                         , '-'                           , '-'                           ]
lab       = ['Multi ' + r'($N_{K} = 64$)', 'Single ' + r'($N_{K} = 64$)' , 'Single ' + r'($N_{K} = 128$)']
c = [0, 1, -1]
for i in range(len(ID)):

    filename = gv.dataDirectory + 'tovStar/' \
                 + '{:}{:}_CentralDensityVersusTime.dat' \
                   .format(ID[i], dirSuffix[i])
    t, rhoC = np.loadtxt(filename)

    ax.plot(t, 1.0e4 * (rhoC - rhoC[0]) / rhoC[0], ls[i], c = gv.color[c[i]], \
            label = lab[i])
ax.legend(prop=prop)
ax.grid()

fig.supxlabel(r'$t/\mathrm{ms}$')
fig.supylabel(r'$10^{4}\times\left(\bar{\rho}_{<1\,\mathrm{km}}\left(t\right)-\bar{\rho}_{<1\,\mathrm{km}}\left(0\right)\right)/\bar{\rho}_{<1\,\mathrm{km}}\left(0\right)$')
plt.subplots_adjust(hspace = 0)

#plt.show()

figName = gv.paperDirectory + 'Figures/fig.tov.pdf'
#figName = 'fig.tov.pdf'
plt.savefig( figName, dpi = 300 )
print( '\n  Saved {:}'.format( figName ) )

import os
os.system('rm -rf __pycache__')

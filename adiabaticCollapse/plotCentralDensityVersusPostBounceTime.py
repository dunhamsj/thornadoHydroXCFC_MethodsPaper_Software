#!/usr/bin/env python3

from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
plt.style.use( '../publication.sty' )

import globalVariables as gv

dataDirectory = gv.dataDirectory + 'adiabaticCollapse/processedData/'

saveFig = False
figName \
  = gv.paperDirectory \
      + 'Figures/fig.CentralDensityVersusPostBounceTime.pdf'
figName = 'fig.CentralDensityVersusPostBounceTime.png'

suffix = [ \
 '_AMR_dr0.25km', \
 '_AMR_dr0.50km', \
 '_Uni_dr0.50km', \
 '_AMR_dr1.00km', \
 '_Uni_dr1.00km' \
]

fig, ax = plt.subplots( 1, 1 )

tmtbMin = +np.inf
tmtbMax = -np.inf

color = gv.color
c = [ color[2], color[0], color[0], color[1], color[1] ]
for s in range( len( suffix ) ):

    filename  = dataDirectory + 'CentralValues{:}.dat'.format( suffix[s] )
    tmtb, DC, TC, YC, SC = np.loadtxt( filename )

    tau = tmtb + 0.6

    ind = np.where( tau > 0.0 )[0]

    tmtbMin = min( tmtbMin, tau[ind].min() )
    tmtbMax = max( tmtbMax, tau[ind].max() )

    yD = DC[ind]

    if ( 'AMR' in suffix[s] ) :
        ls = '-'
    else:
        ls = '--'

    ax.plot( tau[ind], yD, color = c[s], ls = ls, \
             label = '{:}'.format( suffix[s][1:] ) )

ax.set_xlabel( r'$t-\left(t_{\mathrm{b}}-0.6\right)\ \left[\mathrm{ms}\right]$' )

ax.set_ylabel( r'$\rho_{\mathrm{c}}\ \left[\mathrm{g\,cm}^{-3}\right]$' )

ax.set_xscale( 'log' )

ax.legend()

if ( not saveFig ) :
    plt.show()
else:
    plt.savefig( figName, dpi = 300 )
    print( '\n  Saved {:}'.format( figName ) )

import os
os.system( 'rm -rf __pycache__' )

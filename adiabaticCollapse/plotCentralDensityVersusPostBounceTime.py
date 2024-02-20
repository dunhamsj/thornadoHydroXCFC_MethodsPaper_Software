#!/usr/bin/env python3

from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
plt.style.use( '../publication.sty' )

import GlobalVariables.Settings as gvS
gvS.PlotDirectory = '../../thornadoHydroXCFC_MethodsPaper_Data/'

saveFig = True

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

# Found by running plotShockTrajectory.py
#AMR_dr0.25km 2783 278.3996622767047
#AMR_dr0.50km 2609 260.9987130129583
#Uni_dr0.50km 2685 268.5979481437816
#AMR_dr1.00km 2290 229.09799441925597
#Uni_dr1.00km 2331 233.19822607191577
tMax = [ \
         278.4, \
         261.0, \
         268.6, \
         229.1, \
         233.2 \
        ]

# colorblind-friendly palette: https://gist.github.com/thriveth/8560036
color = ['#377eb8', '#ff7f00', '#4daf4a', \
         '#f781bf', '#a65628', '#984ea3', \
         '#999999', '#e41a1c', '#dede00']

c = [ color[2], color[0], color[0], color[1], color[1] ]
for s in range( len( suffix ) ):

    filename  = 'processedData/CentralValues{:}.dat'.format( suffix[s] )
    tmtb, DC, TC, YC, SC = np.loadtxt( filename )

    tau = tmtb + 0.6

    ind = np.where( ( tau > 0.0 ) & ( tau - 0.6 < tMax[s] ) )[0]

    tmtbMin = min( tmtbMin, tau[ind].min() )
    tmtbMax = max( tmtbMax, tau[ind].max() )

    yD = DC[ind]

    if ( 'AMR' in suffix[s] ) :
        ls = '-'
    else:
        ls = '--'

    ax.plot( tau[ind], yD, color = c[s], ls = ls, \
             label = '{:}'.format( suffix[s][1:] ) )

#ax.set_xlim( tmtbMin - 10.0 , tmtbMax + 10.0 )

ax.set_ylabel( r'$\rho_{\mathrm{c}}\ \left[\mathrm{g\,cm}^{-3}\right]$' )

ax.set_xscale( 'log' )

#ax.set_yscale( 'log' )

yLim = ax.get_ylim()
ax.set_ylim( yLim )

ax.legend()

ax.set_xlabel( r'$t-\left(t_{\mathrm{b}}-0.6\right)\ \left[\mathrm{ms}\right]$' )

if ( not saveFig ) :
    plt.show()
else:
    figName \
      = '/home/kkadoogan/Work/thornadoHydroXCFC_MethodsPaper/\
Figures/fig.CentralDensityVersusPostBounceTime.pdf'
    figName = '/home/kkadoogan/fig.CentralDensityVersusPostBounceTime.png'
    plt.savefig( figName, dpi = 300 )
    print( '\n  Saved {:}'.format( figName ) )

import os
os.system( 'rm -rf __pycache__' )

#!/usr/bin/env python

from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
plt.style.use( '../publication.sty' )
from matplotlib import ticker as mticker

import globalVariables as gv

dataDirectory = gv.dataDirectory + 'adiabaticCollapse/processedData/'

suffix = [ \
'_AMR_dr0.25km', \
'_AMR_dr0.50km', \
'_AMR_dr1.00km' \
]

saveFig = False
figName \
  = '/home/kkadoogan/Work/thornadoHydroXCFC_MethodsPaper/\
Figures/fig.CentralValues.pdf'
figName = 'fig.CentralValues.png'

fig, axs = plt.subplots( 2, 2 )

rhoMin  = +np.inf
rhoMax  = -np.inf
tmtbMin = +np.inf
tmtbMax = -np.inf

for s in range( len( suffix ) ):

    filename  = dataDirectory + 'CentralValues{:}.dat'.format( suffix[s] )
    tmtb, DC, TC, YC, SC = np.loadtxt( filename )

    ind0 = np.where( tmtb < 0.0 )[0]
    ind1 = np.where( tmtb > 0.0 )[0]

    rhoMin  = min( rhoMin , DC  [ind0].min() )
    rhoMax  = max( rhoMax , DC  [ind0].max() )
    tmtbMin = min( tmtbMin, tmtb[ind1].min() )
    tmtbMax = max( tmtbMax, tmtb[ind1].max() )

    yS = ( SC[ind0] - SC[ind0[0]] ) / SC[ind0[0]]
    axs[0,0].semilogx( DC[ind0], yS, label = '{:}'.format( suffix[s][1:] ) )
    yY = ( YC[ind0] - YC[ind0[0]] ) / YC[ind0[0]]
    axs[1,0].semilogx( DC[ind0], yY / 1.0e-5 )

    yS = ( SC[ind1] - SC[ind1[0]] ) / SC[ind0[0]]
    axs[0,1].plot( tmtb[ind1], yS )
    yY = ( YC[ind1] - YC[ind1[0]] ) / YC[ind0[0]]
    axs[1,1].plot( tmtb[ind1], yY / 1.0e-5 )

axs[0,0].set_xlim( 5.0e9, rhoMax )
axs[1,0].set_xlim( 5.0e9, rhoMax )
axs[0,1].set_xlim( 0.0, tmtbMax+10.0 )
axs[1,1].set_xlim( 0.0, tmtbMax+10.0 )

#axs[0,0].set_ylabel( r'$S_{\mathrm{c}}/\mathrm{baryon}\ \left[k_{\mathrm{B}}\right]$' )
#axs[1,0].set_ylabel( r'$Y_{\mathrm{e,c}}\ \left[\right]$' )
axs[0,0].set_ylabel( r'$\left(S_{\mathrm{c}}-S_{\mathrm{c,0}}\right)/S_{\mathrm{c,0}}$' )
axs[1,0].set_ylabel( r'$10^{5}\times\left(Y_{\mathrm{e,c}}-Y_{\mathrm{e,c,0}}\right)/Y_{\mathrm{e,c,0}}$' )

SLim  = [ min( axs[0,0].get_ylim()[0], \
               axs[0,1].get_ylim()[0] ), \
          max( axs[0,0].get_ylim()[1], \
               axs[0,1].get_ylim()[1] ) ]
YeLim = [ min( axs[1,0].get_ylim()[0], \
               axs[1,1].get_ylim()[0] ), \
          max( axs[1,0].get_ylim()[1], \
               axs[1,1].get_ylim()[1] ) ]

axs[0,0].set_ylim( SLim )
axs[0,1].set_ylim( SLim )
axs[1,0].set_ylim( YeLim )
axs[1,1].set_ylim( YeLim )

x0ticks = [ 1.0e10, 1.0e11, 1.0e12, 1.0e13, 1.0e14 ]
for i in range( 2 ):
    axs[i,0].set_xticks( x0ticks )
    axs[i,0].xaxis.set_minor_locator \
      ( mticker.LogLocator( numticks = 999, subs = 'auto' ) )

axs[0,0].set_xticklabels( '' )
axs[0,1].set_xticklabels( '' )

#x1ticks = [ 50, 100, 150, 200, 250 ]
#for i in range( 2 ):
#    axs[i,1].set_xticks( x1ticks )

axs[0,1].set_yticklabels( '' )
axs[1,1].set_yticklabels( '' )

plt.subplots_adjust( hspace = 0.0, wspace = 0.0 )

axs[0,0].legend()

axs[1,0].set_xlabel( r'$\rho_{\mathrm{c}}\ \left[\mathrm{g\,cm}^{-3}\right]$' )
axs[1,1].set_xlabel( r'$t-t_{\mathrm{b}}\ \left[\mathrm{ms}\right]$' )

if ( saveFig ) :
    plt.savefig( figName, dpi = 300 )
    print( '\n  Saved {:}'.format( figName ) )
else:
    plt.show()

import os
os.system( 'rm -rf __pycache__' )

#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
plt.style.use( 'publication.sty' )
from matplotlib import ticker as mticker

import globalVariables as gv

from myUtilitiesModule import getPlotfileNumberArray, readShockRadiusSnapshotsFile

saveFig = False
figName \
  = gv.paperDirectory + 'Figures/fig.AdiabaticCollapse_PostBounce_dr0.50km.pdf'
figName = 'fig.png'

dataDirectory = gv.dataDirectory + 'adiabaticCollapse/processedData/'

ID = 'AdiabaticCollapse_XCFC'

plotfileNameRoot = ID + '.plt'

suffix = [ \
'_Uni_dr0.50km', \
'_AMR_dr0.50km' \
]
dX1_u  = 0.5

fig, axs = plt.subplots( 2, 2 )

ls = [ '-', '--' ]
lw = [ 3.0, 1.0 ]
alpha = [ 0.5, 1.0 ]

for s in range( len( suffix ) ) :

    filename = dataDirectory + 'ShockRadiusSnapshots{:}.dat'.format( suffix[s] )
    snapshots, tmtb, Rsh = readShockRadiusSnapshotsFile( filename )

    lab = suffix[s][1:4]

    plotfileDirectory \
      = gv.dataDirectory \
          + 'adiabaticCollapse/{:}{:}/'.format( ID, suffix[s] )

    plotfileNumberArray \
      = getPlotfileNumberArray( plotfileDirectory, plotfileNameRoot )

    for iSS in range( snapshots.shape[0] ):

        ss = str( plotfileNumberArray[snapshots[iSS]] ).zfill( 8 )

        X1, D  = np.loadtxt( dataDirectory + 'PF_D_{:}_{:}.dat' .format( suffix[s][1:], ss ) )
        X1, T  = np.loadtxt( dataDirectory + 'AF_T_{:}_{:}.dat' .format( suffix[s][1:], ss ) )
        X1, Ye = np.loadtxt( dataDirectory + 'AF_Ye_{:}_{:}.dat'.format( suffix[s][1:], ss ) )
        X1, S  = np.loadtxt( dataDirectory + 'AF_S_{:}_{:}.dat' .format( suffix[s][1:], ss ) )

        if ( ( iSS == snapshots.shape[0]-1 ) ) :
            axs[0,0].plot( X1, D, ls = ls[s], c = gv.color[iSS], lw = lw[s], alpha = alpha[s], label = lab )
        else:
            axs[0,0].plot( X1, D, ls = ls[s], c = gv.color[iSS], lw = lw[s], alpha = alpha[s] )

        if ( s == 0 ) :
            axs[0,1].plot( X1, T , ls = ls[s], c = gv.color[iSS], lw = lw[s], alpha = alpha[s], \
                           label = r'$t-t_{{\mathrm{{b}}}}={:.1f}\,\mathrm{{ms}}$'.format( tmtb[iSS] ) )
        else:
            axs[0,1].plot( X1, T , ls = ls[s], c = gv.color[iSS], lw = lw[s], alpha = alpha[s] )
        axs[1,0].plot( X1, Ye, ls = ls[s], c = gv.color[iSS], lw = lw[s], alpha = alpha[s] )
        axs[1,1].plot( X1, S , ls = ls[s], c = gv.color[iSS], lw = lw[s], alpha = alpha[s] )

axs[0,0].legend()
axs[0,1].legend( loc = 3, fontsize = 8 )
axs[0,0].set_yscale( 'log' )
axs[0,1].set_yscale( 'log' )
axs[0,0].set_ylabel( r'$\rho\ \left[\mathrm{g}\,\mathrm{cm}^{-3}\right]$' )
axs[0,1].set_ylabel( r'$T\ \left[\mathrm{K}\right]$' )
axs[1,0].set_ylabel( r'$Y_{e}$' )
axs[1,1].set_ylabel( r'$S/\mathrm{baryon}\ \left[\mathrm{k}_{\mathrm{B}}\right]$' )

axs[0,0].xaxis.set_tick_params \
  ( which = 'both', top = True, left = True , bottom = True, right = False )
axs[0,1].xaxis.set_tick_params \
  ( which = 'both', top = True, left = True, bottom = True, right = True  )
axs[1,0].xaxis.set_tick_params \
  ( which = 'both', top = True, left = True , bottom = True, right = False )
axs[1,1].xaxis.set_tick_params \
  ( which = 'both', top = True, left = False, bottom = True, right = True  )

axs[0,1].yaxis.set_label_position( 'right' )
axs[1,1].yaxis.set_label_position( 'right' )
axs[0,0].yaxis.tick_left()
axs[0,1].yaxis.tick_right()
axs[1,0].yaxis.tick_left()
axs[1,1].yaxis.tick_right()

xticks = [ 1.0e0, 1.0e1, 1.0e2, 1.0e3 ]
xticklabels = [ r'$10^{0}$', r'$10^{1}$', r'$10^{2}$', r'$10^{3}$' ]

for i in range( axs.shape[0] ):
    for j in range( axs.shape[1] ):
        axs[i,j].set_xlim( 0.0 + 0.25 * dX1_u, 8.0e3 + 2.0e3 )
        axs[i,j].set_xscale( 'log' )
        axs[i,j].grid( axis = 'x')#, which = 'both' )
        axs[i,j].set_xticks( xticks )
        axs[i,j].xaxis.set_minor_locator \
          ( mticker.LogLocator( numticks = 999, subs = 'auto' ) )

axs[0,0].set_xticklabels( '' )
axs[0,1].set_xticklabels( '' )
axs[1,0].set_xticklabels( xticklabels )
axs[1,1].set_xticklabels( xticklabels )

fig.supxlabel( r'$r\ \left[\mathrm{km}\right]$', y = 0.025 )
plt.subplots_adjust( hspace = 0, wspace = 0 )

if ( saveFig ) :
  plt.savefig( figName, dpi = 300 )
  print( '\n  Saved {:}'.format( figName ) )
else:
  plt.show()

import os
os.system( 'rm -rf __pycache__ ' )

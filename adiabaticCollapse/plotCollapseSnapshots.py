#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
plt.style.use( 'publication.sty' )

import GlobalVariables.Settings as gvS
gvS.PlotDirectory = '../../thornadoHydroXCFC_MethodsPaper_Data/'

from Utilities.Files import GetFileNumberArray

suffix = [ '_Uni_dr0.50km', '_AMR_dr0.50km' ]
dX1_u  = 0.5

saveFig = True
saveFigAs \
  = '/home/kkadoogan/Work/thornadoHydroXCFC_MethodsPaper/\
Figures/fig.AdiabaticCollapse_Collapse_dr0.50km.pdf'
#saveFigAs = 'fig.png'

# These come from processedData/DensityDecades<suffix>.dat
snapshots = [ np.array( [ 604, 2072, 2332, 2395, 2411 ], dtype = np.int64 ), \
              np.array( [ 481, 1677, 1918, 1981, 1997 ], dtype = np.int64 ) ]

ID = 'AdiabaticCollapse_XCFC'

plotfileBaseName = ID + '.plt'

# colorblind-friendly palette: https://gist.github.com/thriveth/8560036
color = ['#377eb8', '#ff7f00', '#4daf4a', \
         '#f781bf', '#a65628', '#984ea3', \
         '#999999', '#e41a1c', '#dede00']

fig, axs = plt.subplots( 2, 2 )
axx = axs[1,0].twinx()

ls = [ '-', '--' ]
lw = [ 3.0, 1.0 ]
alpha = [ 0.5, 1.0 ]

for s in range( len( suffix ) ) :

    lab = suffix[s][1:4]

    plotfileDirectory \
      = gvS.PlotDirectory \
          + '{:}{:}/'.format( ID, suffix[s] )

    plotfileArray \
      = GetFileNumberArray \
          ( plotfileDirectory,\
            plotfileBaseName,\
            -1, -1, \
            1 )

    for iSS in range( snapshots[s].shape[0] ):

        ss = str( plotfileArray[snapshots[s][iSS]] ).zfill( 8 )

        X1, D     = np.loadtxt( 'processedData/{:}_PF_D_{:}.dat'    .format( suffix[s][1:], ss ) )
        X1, V1    = np.loadtxt( 'processedData/{:}_PF_V1_{:}.dat'   .format( suffix[s][1:], ss ) )
        X1, Psi   = np.loadtxt( 'processedData/{:}_GF_Psi_{:}.dat'  .format( suffix[s][1:], ss ) )
        X1, Alpha = np.loadtxt( 'processedData/{:}_GF_Alpha_{:}.dat'.format( suffix[s][1:], ss ) )
        X1, T     = np.loadtxt( 'processedData/{:}_AF_T_{:}.dat'    .format( suffix[s][1:], ss ) )

        if ( ( iSS == snapshots[s].shape[0]-1 ) ) :
            axs[0,0].plot( X1, D, ls = ls[s], c = color[iSS], lw = lw[s], alpha = alpha[s], label = lab )
        else:
            axs[0,0].plot( X1, D, ls = ls[s], c = color[iSS], lw = lw[s], alpha = alpha[s] )

        axs[0,1].plot( X1, V1 / 2.99792458e5, ls = ls[s], c = color[iSS], lw = lw[s], alpha = alpha[s] )

        if ( ( iSS == snapshots[s].shape[0]-1 ) & ( s == 0  ) ) :
            axs[1,0].plot( X1, Psi, ls = ls[s], c = color[iSS], lw = lw[s], alpha = alpha[s], label = r'$\psi$' )
        else:
            axs[1,0].plot( X1, Psi, ls = ls[s], c = color[iSS], lw = lw[s], alpha = alpha[s] )
        if ( ( iSS == snapshots[s].shape[0]-1 ) & ( s == 0  ) ) :
            axx.plot( X1, Alpha, ls = ls[s], c = color[iSS], lw = lw[s], alpha = alpha[s], label = r'$\alpha$' )
        else:
            axx.plot( X1, Alpha, ls = ls[s], c = color[iSS], lw = lw[s], alpha = alpha[s] )

        axs[1,1].plot( X1, T, ls = ls[s], c = color[iSS], lw = lw[s], alpha = alpha[s] )

    axs[1,0].axhline( 1.0, color = 'k' )

axx.xaxis.set_visible( False )
axx.yaxis.set_visible( False )
ylim1 = axs[1,0].get_ylim()
ylim2 = axx     .get_ylim()

ymin = min( min( ylim1 ), min( ylim2 ) )
ymax = max( max( ylim1 ), max( ylim2 ) )

axs[1,0].set_ylim( ymin, ymax )
axx     .set_ylim( ymin, ymax )

axs[0,0].set_yscale( 'log' )
axs[1,1].set_yscale( 'log' )
axs[1,0].legend()
axx     .legend( loc = (0.735,0.45) )
axs[0,0].legend()
axs[0,0].set_ylabel( r'$\rho\ \left[\mathrm{g}\,\mathrm{cm}^{-3}\right]$' )
axs[0,1].set_ylabel( r'$v/c$' )
axs[1,1].set_ylabel( r'$T\ \left[\mathrm{K}\right]$' )

axs[0,0].xaxis.set_tick_params \
  ( which = 'both', top = True, left = True , bottom = True, right = False )
axs[0,1].xaxis.set_tick_params \
  ( which = 'both', top = True, left = False, bottom = True, right = True  )
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

axs[0,0].set_xticklabels( '' )
axs[0,1].set_xticklabels( '' )
axs[1,0].set_xticklabels( xticklabels )
axs[1,1].set_xticklabels( xticklabels )

fig.supxlabel( r'$r\ \left[\mathrm{km}\right]$', y = 0.025 )
plt.subplots_adjust( hspace = 0, wspace = 0 )

if saveFig:
  plt.savefig( saveFigAs, dpi = 300 )
  print( '\n  Saved {:}'.format( saveFigAs ) )
else:
  plt.show()

import os
os.system( 'rm -rf __pycache__ ' )

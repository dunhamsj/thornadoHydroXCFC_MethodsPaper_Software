#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
plt.style.use( '../publication.sty' )

import globalVariables as gv

from myUtilitiesModule import getPlotfileNumberArray, getMesh_1d, getFieldData

#### ========== User Input ==========

problemName = 'SedovTaylorBlastWave_Relativistic'

nDetCells = '03'

xlabel = r'$r$'

iSS = -1

field   = [ 'PF_D', \
            'PF_V1', \
            'AF_P' ]
ylabel  = [ r'$\rho / \rho_{0}$', \
            r'$v    / v_{0}$', \
            r'$p    / p_{0}$' ]
ylabel_ref = [ r'$\rho_{\mathrm{ref}} / \rho_{0}$', \
                r'$v_{\mathrm{ref}}    / v_{0}$', \
                r'$p_{\mathrm{ref}}    / p_{0}$' ]
norm    = [ 5.0e3, \
            1.0e-3, \
            1.0e-3 ]

xlim = np.array( [ -0.05, 1.05 ] )

plotGrid = False

# Max level of refinement to plot (-1 plots leaf elements)
maxLevel = -1

# Use custom limts for y-axis
useCustomLimits = False
vmin = 0.0
vmax = 2.0

# Save figure (True) or plot figure (False)
saveFig = True

figName = gv.paperDirectory + 'Figures/fig.stbw_1d.pdf'

#### ====== End of User Input =======

# Specify directory containing amrex plotfiles
plotfileDirectoryRoot = gv.dataDirectory
plotfileDirectory = plotfileDirectoryRoot + 'sedovTaylorBlastWave/stbw_1d/'

# Specify plot file base name
plotfileNameRoot = problemName + '.plt'

plotfileNumberArray \
  = getPlotfileNumberArray \
      ( plotfileDirectory,\
        plotfileNameRoot )

plotfileName \
  = plotfileDirectory \
      + '{:}{:}'.format( plotfileNameRoot, \
                         str( plotfileNumberArray[iSS] ).zfill( 8 ) )

fig, ax = plt.subplots( 1, 1 )

data = np.loadtxt( 'spherical_standard_omega0p00_nDetCells{:}_t500.dat' \
                   .format( nDetCells ), skiprows = 2 )
x     = data[:,1]
den   = data[:,2]
press = data[:,4]
vel   = data[:,5]
ref   = [ x, den, vel, press ]

X1_C, X2_C, X3_C, dX1, dX2, dX3, xL, xH, time \
  = getMesh_1d( plotfileName, 'spherical', returnTime = True )

for i in range( len( field ) ):

    data \
      = getFieldData( plotfileName, \
                      field[i], \
                      X1_C, X2_C, X3_C )

    if ( plotGrid and i == 0 ) :
        ax.plot( X1_C, np.ones( X1_C.shape[0] ) * data.max(), \
                 'k.', label = 'mesh' )

    ax.plot( X1_C    , data       / norm[i], '.', c = gv.color[i], \
             label = ylabel[i] )
    ax.plot( ref[0], ref[i+1] / norm[i], '-', c = gv.color[i], \
             label = ylabel_ref[i] )

if useCustomLimits: ax.set_ylim( vmin, vmax )

ylim = ax.get_ylim()

ax.legend( loc = 2 )
ax.grid()

ax.set_xlim( xlim )

ax.set_xlabel( xlabel )

ax.text \
  ( 0.45, 0.875 * ( ylim[1] - ylim[0] ), \
    r'$t = {:}$'.format( np.int64( time ) ), \
    bbox = dict( facecolor = 'white', edgecolor = 'black', \
                 boxstyle = 'round' ) )

if ( saveFig ) :

    plt.savefig( figName, dpi = 300 )
    print( '\n  Saved {:}'.format( figName ) )

else:

    plt.show()

plt.close()

import os
os.system( 'rm -rf __pycache__ ' )

#!/usr/bin/env python3

import numpy as np
from sys import argv
import matplotlib.pyplot as plt
plt.style.use( '../publication.sty' )

import globalVariables as gv

from myUtilitiesModule import getPlotfileNumberArray, getMesh_1d, getFieldData

#### ========== User Input ==========

problemName = 'SedovTaylorBlastWave_XCFC'

nDetCells = '03'

xlabel = r'$r$'

iSS = -1

field  = [ 'PF_D'   , 'PF_V1']#, 'AF_P' ]
ylabel = [ r'$\rho / 5000$', r'$v / 0.001$' ]#, r'$p$' ]
norm   = [ 5.0e3    , 1.0e-3 ]#, 1.0 ]

xlim = np.array( [ -0.1, 1.1 ] )

plotGrid = False

# Max level of refinement to plot (-1 plots leaf elements)
maxLevel = -1

# Use custom limts for y-axis
useCustomLimits = False
vmin = 0.0
vmax = 2.0

# Save figure (True) or plot figure (False)
saveFig = True

figName = 'fig.stbw_1d_nDetCells{:}.pdf'.format( nDetCells )

#### ====== End of User Input =======

# Specify directory containing amrex plotfiles
plotfileDirectoryRoot = gv.dataDirectory
plotfileDirectory \
  = plotfileDirectoryRoot \
      + 'sedovTaylorBlastWave/{0:}_1D_nDetCells{1:}/' \
        .format( problemName, nDetCells )

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
press = data[:,3] * ( 4.0 / 3.0 - 1.0 )
vel   = data[:,5]
exact = [ x, den, vel, press ]

X1_C, X2_C, X3_C, dX1, dX2, dX3, xL, xH, time \
  = getMesh_1d( plotfileName, returnTime = True )

for i in range( len( field ) ):

    data \
      = getFieldData( plotfileName, \
                      field[i], \
                      X1_C, X2_C, X3_C )

    if ( plotGrid and i == 0 ) :
        ax.plot( X1_C, np.ones( X1_C.shape[0] ) * data.max(), \
                 'k.', label = 'mesh' )

    ax.plot( exact[0], exact[i+1] / norm[i], '-', c = gv.color[i] )
    ax.plot( X1_C    , data       / norm[i], '.', c = gv.color[i], \
             label = ylabel[i] )

if useCustomLimits: ax.set_ylim( vmin, vmax )

ylim = ax.get_ylim()

ax.legend()
ax.grid()

ax.set_xlim( xlim )

ax.set_xlabel( xlabel, fontsize = 15 )

ax.text \
  ( 0.9, 0.75 * ( ylim[1] - ylim[0] ), \
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

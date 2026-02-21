#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
plt.style.use( '../publication.sty' )

import globalVariables as gv

from myUtilitiesModule import getPlotfileNumberArray, getMesh_1d, getFieldData

#### ========== User Input ==========

problemNameRoot = 'RiemannProblem1D_Sod'
suffix = [ '_nX0256', '_nX0016_AMR_FCT']#, '_nX0016_AMR_FCF' ]
leglabel = [ r'$N_{K} = 256$', 'AMR (On)]#', 'AMR (Off)' ]

xlabel = r'$x$'

iSS = -1

field   = [ 'PF_D', \
            'PF_V1', \
            'AF_P' ]
ylabel  = [ r'$\rho$', \
            r'$v$', \
            r'$p$' ]

xlim = np.array( [ -0.02, 1.02 ] )

saveFig = True

figName = gv.paperDirectory + 'Figures/fig.sod.pdf'

#### ====== End of User Input =======

# Specify directory containing amrex plotfiles
plotfileDirectoryRoot = gv.dataDirectory
plotfileDirectory = plotfileDirectoryRoot + 'Sod/'

fig, axs = plt.subplots( 3, 1 )

data = np.loadtxt( plotfileDirectory + 'sod.dat', skiprows = 1 )
x     = data[:,0]
press = data[:,1]
den   = data[:,2]
vel   = data[:,3]
exact = [ x, den, vel, press ]

for i in range( len( suffix ) ) :

    plotfileNameRoot = problemNameRoot + suffix[i] + '.plt'
    
    plotfileNumberArray \
      = getPlotfileNumberArray \
          ( plotfileDirectory,\
            plotfileNameRoot )
    
    plotfileName \
      = plotfileDirectory \
          + '{:}{:}'.format( plotfileNameRoot, \
                             str( plotfileNumberArray[iSS] ).zfill( 8 ) )


    X1_C, X2_C, X3_C, dX1, dX2, dX3, xL, xH, time \
      = getMesh_1d( plotfileName, 'cartesian', returnTime = True )

    print( 'Number of elements: {:}'.format( X1_C.shape[0] ) )

    for j in range( len( field ) ):
    
        data \
          = getFieldData( plotfileName, \
                          field[j], \
                          X1_C, X2_C, X3_C )
    
        if ( i == 0 ) :
            axs[j].set_ylabel( ylabel[j] )
            axs[j].grid()
            axs[j].set_xlim( xlim )
            axs[j].plot( exact[0], exact[j+1], 'k-', label = 'Exact' )

        axs[j].plot( exact[0], exact[j+1], 'k-' )

        axs[j].plot( X1_C    , data      , '.', c = gv.color[i], \
                     label = leglabel[i] )

axs[0].legend( loc = 1 )
axs[-1].set_xlabel( xlabel, fontsize = 15 )

for i in range( len( field ) - 1 ) :
    axs[i].xaxis.set_ticklabels( [] )

plt.subplots_adjust( hspace = 0.0 )

if ( saveFig ) :

    plt.savefig( figName, dpi = 300 )
    print( '\n  Saved {:}'.format( figName ) )

else:

    plt.show()

plt.close()

fig, ax = plt.subplots( 1, 1 )

for i in range( len( suffix ) ) :

    plotfileName = plotfileDirectory + problemNameRoot + suffix[i] + '.Tally_BaryonicMass.dat'

    data = np.loadtxt(plotfileName, skiprows = 1)
    time = data[:,0]
    dm = np.abs(data[:,-1] / data[0,3])

    ax.grid()

    ax.semilogy( time, dm, '.', c = gv.color[i], label = leglabel[i] )

ax.legend( loc = 1 )
ax.set_xlabel( 'time', fontsize = 15 )
ax.set_ylabel( r'$\left|M\left(t\right) - M\left(0\right)\right| / M\left(0\right)$' )

figName = gv.paperDirectory + 'Figures/fig.sod_conservation.pdf'
figName = 'fig.sod_conservation.pdf'
if ( saveFig ) :

    plt.savefig( figName, dpi = 300 )
    print( '\n  Saved {:}'.format( figName ) )

else:

    plt.show()

plt.close()

import os
os.system( 'rm -rf __pycache__ ' )

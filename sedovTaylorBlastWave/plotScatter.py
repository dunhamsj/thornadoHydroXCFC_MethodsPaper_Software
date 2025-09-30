#!/usr/bin/env python3

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import yt
yt.funcs.mylog.setLevel(40) # Suppress yt warnings

plt.style.use( '../publication.sty' )

import globalVariables as gv

from myUtilitiesModule import getPlotfileNumberArray

### Beginning of user input ###

saveFig = True

# Specify name of problem
problemName = 'SedovTaylorBlastWave_XCFC'

iSS = -1

nDetCells = '03'

field   = [ 'PF_D', \
            'PF_V', \
            'AF_P' ]
ylabel  = [ r'$\rho / \rho_{0}$', \
            r'$v    / v_{0}$', \
            r'$p    / p_{0}$' ]
ylabelExact = [ r'$\rho_{\mathrm{Exact}} / \rho_{0}$', \
                r'$v_{\mathrm{Exact}}    / v_{0}$', \
                r'$p_{\mathrm{Exact}}    / p_{0}$' ]
norm    = [ 5.0e3, \
            1.0e-3, \
            1.0e-3 ]

xlim = np.array( [ -0.1, 1.1 ] )

figName = '/home/dunhamsj/fig.stbw_scatter_nDetCells{:}.pdf'.format( nDetCells )

# Specify directory containing amrex plotfiles
plotfileDirectoryRoot = gv.dataDirectory

# Specify plot file base name
plotfileNameRoot = problemName + '.plt'

plotfileDirectory \
  = [ plotfileDirectoryRoot \
        + 'sedovTaylorBlastWave/{0:}_2D_nDetCells{1:}/' \
          .format( problemName, nDetCells ), \
      plotfileDirectoryRoot \
        + 'sedovTaylorBlastWave/{0:}_3D_nDetCells{1:}/' \
          .format( problemName, nDetCells ) ]
plotfileDirectory \
  = [ plotfileDirectoryRoot \
        + 'sedovTaylorBlastWave/{0:}_2D_nDetCells{1:}/' \
          .format( problemName, nDetCells ) ]

### End of user input ###

fig, ax = plt.subplots()

bl = 'boxlib'

marker = [ '.', 'x' ]
for i in range( len( plotfileDirectory ) ) :

    plotfileNumberArray \
      = getPlotfileNumberArray \
          ( plotfileDirectory[i],\
            plotfileNameRoot )
    
    plotfileName \
      = plotfileDirectory[i] \
          + '{:}{:}'.format( plotfileNameRoot, \
                             str( plotfileNumberArray[iSS] ).zfill( 8 ) )
    
    ds = yt.load( plotfileName )
    
    time = ds.current_time.to_ndarray()

    # Get lower and higher boundaries and convert them to numpy arrays
    xL = ds.domain_left_edge.to_ndarray()
    xH = ds.domain_right_edge.to_ndarray()

    for j in range( len( field ) ) :

        if ( field[j] == 'PF_V' ) :
            blField1 = (bl,field[j]+'1')
            blField2 = (bl,field[j]+'2')
            blField3 = (bl,field[j]+'3')
        else:
            blField = (bl,field[j])
        
        ad = ds.all_data()
        x  = ad['X1_C'].to_ndarray()
        y  = ad['X2_C'].to_ndarray()
        z  = ad['X3_C'].to_ndarray()
        dx = ad['dX1' ].to_ndarray()
        dy = ad['dX2' ].to_ndarray()
        dz = ad['dX3' ].to_ndarray()
        if ( field[j] == 'PF_V' ) :
            V1 = ad['PF_V1'].to_ndarray()
            V2 = ad['PF_V2'].to_ndarray()
            V3 = ad['PF_V3'].to_ndarray()
            if ( '2D' in plotfileDirectory[i] ) :
                d = np.sqrt( V1**2 + V2**2 )
            else:
                d = np.sqrt( V1**2 + V2**2 + V3**2 )
        else:
            d  = ad[field[j]].to_ndarray()
        delta = 1.0e10

        if ( '2D' in plotfileDirectory[i] ) :
            r = np.sqrt( x**2 + y**2 )
        else:
            r = np.sqrt( x**2 + y**2 + z**2 )

        ind = np.where( r <= 1.0 )[0]
        r = r[ind]
        d  = d[ind]
        if ( i == 0 ) :
            ax.scatter( r, d / norm[j], marker = marker[i], c = gv.color[j], \
                        label = ylabel[j] )
        else:
            ax.scatter( r, d / norm[j], marker = marker[i], c = gv.color[j] )

data = np.loadtxt( 'spherical_standard_omega0p00_nDetCells03_t500.dat', \
                   skiprows = 2 )
x     = data[:,1]
den   = data[:,2]
press = data[:,4]
vel   = data[:,5]
color = [ 'gold', 'blue', 'magenta' ]
ax.plot( x, den   / norm[0], '-', c = color[0], label = ylabelExact[0] )
ax.plot( x, vel   / norm[1], '-', c = color[1], label = ylabelExact[1]  )
ax.plot( x, press / norm[2], '-', c = color[2], label = ylabelExact[2]  )

ax.grid()
ax.legend( loc = 2 )

ylim = ax.get_ylim()
ax.text \
  ( 0.45, 0.9 * ( ylim[1] - ylim[0] ), \
    r'$t = {:}$'.format( np.int64( time ) ), \
    bbox = dict( facecolor = 'white', edgecolor = 'black', \
                 boxstyle = 'round' ) )

ax.set_xlabel( r'$r$' )
ax.set_xlim( xlim )

if ( saveFig ) :
    plt.savefig( figName, dpi = 300 )
    print( '\n   Saved {:}'.format( figName ) )
else:
    plt.show()

#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import yt
yt.funcs.mylog.setLevel(40) # Suppress yt warnings

plt.style.use( '../publication.sty' )

import globalVariables as gv

from myUtilitiesModule import getPlotfileNumberArray

### Beginning of user input ###

saveFig = True

problemName = 'SedovTaylorBlastWave_Relativistic'

iSS = -1

nDetCells = '03'

field   = [ 'PF_D', \
            'PF_V', \
            'AF_P' ]
mklabel = [ '3D', '2D' ]
ylabel  = [ r'$\rho / \rho_{0}$', \
            r'$v    / v_{0}$', \
            r'$p    / p_{0}$' ]
ylabel_ref = r'$\mathrm{ref}$'
norm    = [ 5.0e3, \
            1.0e-3, \
            1.0e-3 ]

xlim = np.array( [ -0.1, 1.1 ] )

# Specify directory containing amrex plotfiles
plotfileDirectoryRoot = gv.dataDirectory

# Specify plot file base name
plotfileNameRoot = problemName + '.plt'

plotfileDirectory \
  = [ plotfileDirectoryRoot \
        + 'sedovTaylorBlastWave/stbw_{0:}/' \
          .format( i.lower() ) for i in mklabel ]

### End of user input ###

ref = np.loadtxt( \
  'spherical_standard_omega0p00_nDetCells{:}_t500.dat'.format( nDetCells ), \
  skiprows = 2 )
xEx   = ref[:,1]
den   = ref[:,2]
press = ref[:,4]
vel   = ref[:,5]
ref = [ den, vel, press ]
color = gv.color#[ 'gold', 'blue', 'magenta' ] # complementary to gv.color

for j in range( len( field ) ) :

    fig, ax = plt.subplots()

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

        ad = ds.all_data()
        x = ad['X1_C'].to_ndarray()
        y = ad['X2_C'].to_ndarray()

        if ( '2d' in plotfileDirectory[i] ) :
            r = np.sqrt( x**2 + y**2 )
        else:
            z = ad['X3_C'].to_ndarray()
            r = np.sqrt( x**2 + y**2 + z**2 )

        # Restrict domain to 0 <= r <= 1
        ind = np.random.randint( 0, r.shape[0], 1000 )
        ind = np.where( r <= 1.0 )[0]
        r = r[ind]

        if ( field[j] == 'PF_V' ) :
            V1 = ad['PF_V1'].to_ndarray()[ind]
            V2 = ad['PF_V2'].to_ndarray()[ind]
            if ( '2d' in plotfileDirectory[i] ) :
                d = np.sqrt( V1**2 + V2**2 )
            else:
                V3 = ad['PF_V3'].to_ndarray()[ind]
                d = np.sqrt( V1**2 + V2**2 + V3**2 )
        else:
            d = ad[field[j]].to_ndarray()[ind]

        ax.scatter( r, d / norm[j], \
                    color = gv.color[i], \
                    marker = '.', \
                    label = mklabel[i], \
                    rasterized = True )

    y = [ ex / norm[j] for ex in ref[j] ]
    ax.plot( xEx, y, 'k-', label = ylabel_ref )

    ax.grid()
    ax.legend( loc = 2 )

    ylim = ax.get_ylim()
    ax.text \
      ( 0.45, 0.875 * ( ylim[1] - ylim[0] ), \
        r'$t = {:}$'.format( np.int64( time ) ), \
        bbox = dict( facecolor = 'white', edgecolor = 'black', \
                     boxstyle = 'round' ) )
    
    ax.set_xlabel( r'$r$' )
    ax.set_xlim( xlim )

    ax.set_ylabel( ylabel[j] )

    if ( saveFig ) :
        figName = gv.paperDirectory + 'Figures/fig.stbw_scatter_{:}.pdf' \
                  .format( field[j] )
        plt.savefig( figName, dpi = 300 )
        print( '\n   Saved {:}'.format( figName ) )
    else:
        plt.show()

    plt.close()

import os
os.system( 'rm -rf __pycache__ ' )

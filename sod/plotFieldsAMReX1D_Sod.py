#!/usr/bin/env python3

import numpy as np
from sys import argv
import matplotlib.pyplot as plt
plt.style.use( '../publication.sty' )
import yt

import globalVariables as gv

from myUtilitiesModule import getPlotfileNumberArray, getMesh_1d, getFieldData

problemName = 'RiemannProblem1D_Sod'

figTitle = '{:}'.format( problemName )

plotfileDirectory \
 = '/mnt/shared/work/codes/thornado/SandBox/\
AMReX/dgExperiments_Euler_Relativistic_IDEAL/'

plotfileNameRoot = problemName + '.plt'

plotfileNumberArray \
  = getPlotfileNumberArray \
      ( plotfileDirectory,\
        plotfileNameRoot )

field = 'CF_D'

def getDataIC( iSS, maxLevel = -1, nXpp = [0,0,0], refD = -1.0, saveFig = False, sSfx = '' ):

    fig, ax = plt.subplots( 1, 1 )

    plotfileName \
      = plotfileDirectory \
          + '{:}{:}'.format( plotfileNameRoot, \
                             str( plotfileNumberArray[iSS] ).zfill( 8 ) )

    if ( maxLevel != -1 ) :

        ds = yt.load( '{:}'.format( plotfileName ) )
        nX = ds.domain_dimensions
        xL = ds.domain_left_edge
        
        for iLevel in range( maxLevel + 1 ) :

            nXp = nXpp[iLevel]

            nXX = np.array( [ nX[0]+nXp, nX[1], nX[2] ], np.int64 )
    
            coveringGrid \
              = ds.covering_grid \
                  ( level           = iLevel, \
                    left_edge       = xL, \
                    dims            = nXX, \
                    num_ghost_zones = 0 )
        
            data = coveringGrid[field].to_ndarray()[:,0,0]
            X1_C = coveringGrid['X1_C'].to_ndarray()[:,0,0]
            dX1  = coveringGrid['dX1'].to_ndarray()[:,0,0]

            ax.plot( X1_C, data, '.', c = gv.color[iLevel] )

    else :

        X1_C, X2_C, X3_C, dX1, dX2, dX3, xL, xH, time \
          = getMesh_1d( plotfileName, 'cartesian', returnTime = True )
    
        data \
          = getFieldData( plotfileName, \
                          field, \
                          X1_C, X2_C, X3_C )

        # Find and plot refinement boundaries
        ddx = np.diff( dX1 )
        ind = np.where( ddx > 0.0 )[0]
        xRef = []
        for i in range( ind.shape[0] ):
            xRef.append( X1_C[ind[i]] + 0.5 * dX1[ind[i]] )
            ax.axvline( xRef[i] )

        ax.plot( X1_C, data, 'k.' )

#    # Plot mesh
#    for i in range( X1_C.shape[0] ):
#        ax.axvline( X1_C[i] - 0.5 * dX1[i], c = 'k' )
#    ax.axvline( X1_C[X1_C.shape[0]-1] + 0.5 * dX1[X1_C.shape[0]-1], c = 'k' )

    ax.grid()

    if ( refD > -1.0 ) :
        ax.axhline( refD, c = 'r' )

    ax.set_xlim( -0.05, 1.05 )
    ax.set_ylim( 0.05, 1.05 )
    ax.set_xlabel( r'$x$' )
    ax.set_ylabel( 'CF_D' )

    figName = '/home/dunhamsj/thornado_group_meeting_presentation/fig.sod_{:}.png'.format( sSfx )

    if ( saveFig ) :
    
        plt.savefig( figName, dpi = 300 )
        print( '\n  Saved {:}'.format( figName ) )
    
    else:
    
        plt.show()
    
    plt.close()

    return
#iSS = 0
#sSfx = [ '0'    , '1'    , '2'    , '3'    , '4'     , '5'    , '6'    , '7' ]
#mL   = [ 0      , 0      , 1      , 1      , 2       , 2      , 2      , -1  ]
#refD = [ -1.0   , +0.2   , -1.0   , +0.7   , -1.0    , +0.7   , -1.0   , -1.0 ]
#nXp  = [ [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,16], [0,0,16], [0,4,16], [0,0,0]  ]
#for i in range( 7,8):#len( sSfx ) ):
#    getDataIC( iSS, maxLevel = mL[i], nXpp = nXp[i], refD = refD[i], \
#               saveFig = True, sSfx = sSfx[i] )

def getDataLateTime( iSS, xRefOld = [], saveFig = False, sSfx = '8', t = -1.0, mixData = False ):

    fig, ax = plt.subplots( 1, 1 )

    plotfileName \
      = plotfileDirectory \
          + '{:}{:}'.format( plotfileNameRoot, \
                             str( plotfileNumberArray[iSS] ).zfill( 8 ) )

    # Get refinement boundaries
    X1_C, X2_C, X3_C, dX1, dX2, dX3, xL, xH, time \
      = getMesh_1d( plotfileName, 'cartesian', returnTime = True )
    if ( t < 0.0 ) :
        t = time
    data \
      = getFieldData( plotfileName, \
                      field, \
                      X1_C, X2_C, X3_C )

    ddx = np.diff( dX1 )
    ind = np.where( ddx > 0.0 )[0]

    xRefN = []
    for i in range( ind.shape[0] ):
        xRefN.append( X1_C[ind[i]] + 0.5 * dX1[ind[i]] )

    if ( not xRefOld ) :
        ax.axvline( xRefN[0] , c = 'k', label = r'$t = {:.2f}$'.format( t ) )
        ax.axvline( xRefN[1] , c = 'k' )
        xRefOld = xRefN
    else:
        ax.axvline( xRefOld [0] , c = 'k', label = r'$t = {:.2f}$'.format( t ), alpha = 0.5 )
        ax.axvline( xRefOld [1] , c = 'k', alpha = 0.5 )
        ax.axvline( xRefN[0] , c = 'k', label = r'$t = {:.2f}$'.format( time ) )
        ax.axvline( xRefN[1] , c = 'k' )

    ds = yt.load( '{:}'.format( plotfileName ) )
    
    xL = ds.domain_left_edge

    c = gv.color
    
    nX = ds.domain_dimensions

    for iLevel in range( 3 ):

        if ( mixData ) :

            coveringGrid \
              = ds.covering_grid \
                  ( level           = iLevel, \
                    left_edge       = xL, \
                    dims            = nX * 2**iLevel, \
                    num_ghost_zones = 0 )
            
            data_on_level = coveringGrid[field].to_ndarray()[:,0,0]
            X1_C_on_level = coveringGrid['X1_C'].to_ndarray()[:,0,0]
            dX1_on_level = coveringGrid['dX1'].to_ndarray()[:,0,0]
        
#            ax.plot( X1_C_on_level[ind], data_on_level[ind], '.', c = gv.color[iLevel] )

            x = np.empty( nX[0] * 2**iLevel, np.float64 )
            x[0] = 0.5 * dX1_on_level[0]
            xx = [np.array( [x[0],0.0,0.0] )]
            for i in range( 1, nX[0] * 2**iLevel ):
                x[i] = x[i-1] + dX1_on_level[0]
                xx.append( np.array( [x[i], 0.0, 0.0] ) )

            if ( iLevel == 0 ) :
                ind = np.where( x > xRefOld[1] )[0]
            if ( iLevel == 1 ) :
                ind = np.where( ( x > xRefOld[0] ) & ( x < xRefOld[1] ) )[0]
            if ( iLevel == 2 ) :
                ind = np.where( x < xRefOld[0] )[0]
    
            data \
              = np.copy( ds.find_field_values_at_points(("boxlib",field), \
                         xx ) )
            for i in range( data.shape[0] ):
                if ( data[i] == data[i-1] and i < data.shape[0]-1 ) :
                    data[i] = 0.5 * ( data[i-1] + data[i+1] )
            ax.plot( x[ind], data[ind], '.', c = gv.color[iLevel] )

        if ( not mixData ) :

            if ( iLevel == 0 ) :
                ind = np.where( X1_C > xRefN[1] )[0]
            if ( iLevel == 1 ) :
                ind = np.where( ( X1_C > xRefN[0] ) & ( X1_C < xRefN[1] ) )[0]
            if ( iLevel == 2 ) :
                ind = np.where( X1_C < xRefN[0] )[0]
    
            ax.plot( X1_C[ind], data[ind], \
                     ls = 'none', \
                     color = gv.color[iLevel], \
                     marker = '.' )
#    # Plot mesh
#    for i in range( X1_C.shape[0] ):
#        ax.axvline( X1_C[i] - 0.5 * dX1[i], c = 'k' )
#    ax.axvline( X1_C[X1_C.shape[0]-1] + 0.5 * dX1[X1_C.shape[0]-1], c = 'k' )

    ax.set_xlim( -0.05, 1.05 )
    ax.set_ylim( 0.05, 1.05 )
    ax.set_xlabel( r'$x$' )
    ax.set_ylabel( 'CF_D' )

    ax.legend( loc = 3 )

    figName = '/home/dunhamsj/thornado_group_meeting_presentation/fig.sod_{:}.png'.format( sSfx )
    if saveFig:
        plt.savefig( figName, dpi = 300 )
        print( '\n  Saved {:}'.format( figName ) )
    else:
        plt.show()
        plt.close()
    
    return xRefN, time

saveFig = True

xRefOld, tOld = getDataLateTime( -27, saveFig = saveFig, sSfx = '8' )
xRefNew, tNew = getDataLateTime( -3 , xRefOld = xRefOld, saveFig = saveFig, sSfx = '9', mixData = True, t = tOld )
xRefNew, tNew = getDataLateTime( -3 , xRefOld = xRefOld, saveFig = saveFig, sSfx = '10', t = tOld )

import os
os.system( 'rm -rf __pycache__ ' )

#!/usr/bin/env python

import numpy as np
import yt
yt.funcs.mylog.setLevel(40) # Suppress yt warnings

def getPlotfileNumberArray \
      ( plotfileDirectory, plotfileNameRoot, swa = False ):

    from os import listdir

    lenS = len( plotfileNameRoot )

    # Create list of all files in plotfileDirectory
    plotfileArray \
      = np.sort( np.array( \
          [ convert( file ) for file in listdir( plotfileDirectory ) ] ) )

    # Filter file list to only those that start with plotfileNameRoot
    plotfileList = []
    for iFile in range( plotfileArray.shape[0] ):

        sFile = plotfileArray[iFile]

        if (not swa):
            if ( sFile[0:lenS] == plotfileNameRoot and sFile[lenS+1].isdigit() ):
                plotfileList.append( np.int64( sFile[lenS:lenS+8] ) )
        else:
            if ( sFile[0:lenS] == plotfileNameRoot and sFile[lenS+1] == 'p' ):
                plotfileList.append( np.int64( sFile[lenS+4:lenS+12] ) )

    plotfileNumbers = np.array( plotfileList )

    # Error out if list is empty
    if ( not plotfileNumbers.shape[0] > 0 ) :

        msg = '\n>>>No files found.\n'
        msg += '>>>Double check the path: {:}\n'.format( plotfileDirectory )
        msg += '>>>Double check the plotfileNameRoot: {:}\n' \
               .format( plotfileNameRoot )
        msg += '>>> Is it plt_ or just plt?\n'

        if ( plotfileNumbers.shape[0] > 0 ) :
            print( msg )
            exit()

    # Sort Numbers
    plotfileNumbers.sort()

    return plotfileNumbers
# end getPlotfileNumberArray

def convert( s ):

    from charade import detect

    """from https://www.geeksforgeeks.org/python-character-encoding/"""

    # if in the charade instance
    if ( isinstance( s, str ) ) :
        s = s.encode()

    # retrieving the encoding information
    # from the detect() output
    encoding = detect(s)['encoding']

    if ( encoding == 'utf-8' ) :
        return s.decode()
    else:
        return s.decode( encoding )
# end convert

def getMesh_1d( File, coordinateSystem, returnTime = False ):

    ds = yt.load( '{:}'.format( File ) )

    nX = ds.domain_dimensions
    xL = ds.domain_left_edge
    xH = ds.domain_right_edge

    X1  = []
    dX1 = []

    for lvl in range( ds.max_level + 1 ):

        grids = ds.index.select_grids( lvl )

        for grid in grids:

            X1_C = grid["boxlib","X1_C"]
            dX1g = grid["boxlib","dX1"]

            for iX1 in range( grid.child_mask.shape[0] ):
                for iX2 in range( grid.child_mask.shape[1] ):
                    for iX3 in range( grid.child_mask.shape[2] ):

                        if ( grid.child_mask[iX1,iX2,iX3] ) :

                            X1 .append( np.float64( X1_C[iX1,iX2,iX3] ) )
                            dX1.append( np.float64( dX1g[iX1,iX2,iX3] ) )
    if ( coordinateSystem.lower() == 'spherical' ):
        X2  = [ np.pi / 2.0 ]
        dX2 = [ np.pi ]
        X3  = [ np.pi ]
        dX3 = [ 2.0 * np.pi ]
    elif ( coordinateSystem.lower() == 'cylindrical' ):
        X2  = [ 0.5 ]
        dX2 = [ 1.0 ]
        X3  = [ np.pi ]
        dX3 = [ 2.0 * np.pi ]
    else:
        X2  = [ 0.5 ]
        dX2 = [ 1.0 ]
        X3  = [ 0.5 ]
        dX3 = [ 1.0 ]

    X1  = np.array( X1  )
    X2  = np.array( X2  )
    X3  = np.array( X3  )
    dX1 = np.array( dX1 )
    dX2 = np.array( dX2 )
    dX3 = np.array( dX3 )

    indX1 = np.argsort( X1 )
    indX2 = np.argsort( X2 )
    indX3 = np.argsort( X3 )

    X1  = np.copy( X1 [indX1] )
    X2  = np.copy( X2 [indX2] )
    X3  = np.copy( X3 [indX3] )

    dX1 = np.copy( dX1[indX1] )
    dX2 = np.copy( dX2[indX2] )
    dX3 = np.copy( dX3[indX3] )

    if ( returnTime ) : time = ds.current_time.to_ndarray()

    del ds

    if ( returnTime ) :
        return X1, X2, X3, dX1, dX2, dX3, xL, xH, time
    else:
        return X1, X2, X3, dX1, dX2, dX3, xL, xH
# end getMesh_1d

def getFieldData( plotFileName, \
                  field, \
                  X1, X2, X3, \
                  returnUnits = False, \
                  yScale = 1.0 ):

    ds = yt.load( '{:}'.format( plotFileName ) )

    nX1 = X1.shape[0]
    nX2 = X2.shape[0]
    nX3 = X3.shape[0]

    locations = [None]*nX1*nX2*nX3
    for k in range( nX3 ):
        for j in range( nX2 ):
            for i in range( nX1 ):
                Here = k*nX1*nX2 + j*nX1 + i
                locations[Here] = [X1[i],X2[j],X3[k]]

    data \
      = np.copy( ds.find_field_values_at_points( ("boxlib",field), locations ) )

    if   ( field == 'PF_V1' ) : dataUnits = 'km/s'
    elif ( field == 'PF_D'  ) : dataUnits = 'g/cm^3'
    elif ( field == 'AF_T'  ) : dataUnits = 'K'
    elif ( field == 'AF_Ye' ) : dataUnits = ''
    elif ( field == 'AF_S'  ) : dataUnits = 'kb/baryon'
    else:                       dataUnits = ''

    data /= yScale

    if ( returnUnits ) :
        return data, dataUnits
    else:
        return data
# end getFieldData

def readDensityDecadesFile( filename ):

    with open( filename, 'r' ) as f:
        f.readline()
        f.readline()
        f.readline()
        indb = f.readline().split(' ')[2]
        tb   = f.readline().split(' ')[2]
        rhob = f.readline().split(' ')[2]
        indd = f.readline().split( '[' )[1].split( ']' )[0].split( ' ' )[1:-1]
        pfnd = f.readline().split( '[' )[1].split( ']' )[0].split( ' ' )[1:-1]

    indb = np.int64  ( indb )
    tb   = np.float64( tb   )
    rhob = np.float64( rhob )
    indd = np.array( indd, dtype = np.int64 )
    pfnd = np.array( pfnd, dtype = np.int64 )

    return indb, tb, rhob, indd, pfnd
# end readDensityDecadesFile

def readShockRadiusSnapshotsFile( filename ):

    with open( filename, 'r' ) as f:
        f.readline()
        f.readline()
        f.readline()
        ss   = f.readline().split( '[' )[1].split( ']' )[0].split( ' ' )[1:-1]
        tmtb = f.readline().split( '[' )[1].split( ']' )[0].split( ' ' )[1:-1]
        Rsh  = f.readline().split( '[' )[1].split( ']' )[0].split( ' ' )[1:-1]

    ss   = np.array( ss  , dtype = np.int64   )
    tmtb = np.array( tmtb, dtype = np.float64 )
    Rsh  = np.array( Rsh , dtype = np.float64 )

    return ss, tmtb, Rsh
# end readShockRadiusSnapshotsFile

def Lagrange( x, xq, i ):
    L = 1.0
    for j in range( xq.shape[0] ):
        if i != j:
            L *= ( x - xq[j] ) / ( xq[i] - xq[j] )
    return L

def rho_h( x, xq, rhoq ):
    rho = 0.0
    for i in range( xq.shape[0] ):
        rho += rhoq[i] * Lagrange( x, xq, i )
    return rho

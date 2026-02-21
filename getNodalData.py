#!/usr/bin/env python

import numpy as np

def getData( dataDirectory, fileNamePrefix, nN ):

    """
    dataDirectory: directory holding the nodal data for each process;
                   e.g., /home/kkadoogan/thornado/SandBox/AMReX/Applications/DynamicTOV_XCFC/DynamicTOV.plt00000000_nodal/
    fileNamePrefix: prefix for nodal data files; e.g., `CF_D` in `CF_D_proc000.dat`
    """

    nProcs = GetNumberOfProcesses( dataDirectory, fileNamePrefix )

    fileNameRoot = dataDirectory + fileNamePrefix

    # Assumes you're working with 1D data
    x1n_G = []
    x1c_G = []
    dx1_G = []
    un_G  = []

    for i in range( nProcs ):

        data \
          = np.loadtxt \
              ( fileNameRoot \
                  + '_proc{:}.dat'.format( str( i ).zfill( 3 ) ) )

        j = 0
        iLevel = np.int64  ( data[:,j]         ); j += 1
        iX1    = np.int64  ( data[:,j]         ); j += 1
        iX2    = np.int64  ( data[:,j]         ); j += 1
        iX3    = np.int64  ( data[:,j]         ); j += 1
        dx1    = np.float64( data[:,j]         ); j += 1
        dx2    = np.float64( data[:,j]         ); j += 1
        dx3    = np.float64( data[:,j]         ); j += 1
        x1n    = np.float64( data[:,j:j+nN[0]] ); j += nN[0]
        x2n    = np.float64( data[:,j:j+nN[1]] ); j += nN[1]
        x3n    = np.float64( data[:,j:j+nN[2]] ); j += nN[2]
        un     = data[:,j:]

        x1c = np.empty(x1n.shape[0], np.float64)
        for iX1 in range(x1c.shape[0]):
          x1c[iX1] = np.sum(x1n[iX1,:]) / np.float64(nN[0])

        x1n = np.copy( x1n.flatten() )
        un  = np.copy( un .flatten() )
        x1c = np.copy( x1c.flatten() )
        dx1 = np.copy( dx1.flatten() )

        x1n_G.append( x1n )
        un_G .append( un  )
        x1c_G.append( x1c )
        dx1_G.append( dx1 )

    flat_x1n = []
    for x1n in x1n_G:
        for xn in x1n:
            flat_x1n.append( xn )

    flat_un = []
    for un in un_G:
        for u in un:
            flat_un.append( u )

    flat_x1c = []
    for x1c in x1c_G:
        for xc in x1c:
            flat_x1c.append( xc )

    flat_dx1 = []
    for dx1 in dx1_G:
        for dx in dx1:
            flat_dx1.append( dx )

    # Assumes you're working with 1D data

    x1n = np.array( flat_x1n )
    un  = np.array( flat_un )

    indX1 = np.argsort( x1n )

    x1n = np.copy( x1n[indX1] )
    un  = np.copy( un [indX1] )

    x1c = np.array( flat_x1c )
    dx1 = np.array( flat_dx1 )

    indX1 = np.argsort( x1c )

    x1c = np.copy( x1c[indX1] )
    dx1 = np.copy( dx1[indX1] )

    return x1n, un, dx1
# END getData

def GetNumberOfProcesses( dataDirectory, fileNamePrefix ):

    from os import listdir

    allFiles = listdir( dataDirectory )
    nProcs = 0
    for file in allFiles:
        if ( fileNamePrefix in file ) : nProcs += 1

    return nProcs
# END GetNumberOfProcesses


def getQuadratureWeights1D( nN ):

    if   nN == 1:
        wq = np.array( [ 1.0 ], np.float64 )
    elif nN == 2:
        wq = np.array( [ 0.5, 0.5 ], np.float64 )
    elif nN == 3:
        wq = np.array( [ 5.0 / 18.0, 8.0 / 18.0, 5.0 / 18.0 ], np.float64 )

    return wq
# getQuadratureWeights1D


if ( __name__ == '__main__' ) :

    # User-defined data

    rootDir = '/home/kkadoogan/Work/Codes/thornado/'
    rootDir += 'SandBox/AMReX/Applications/DynamicTOV_XCFC/'

    # Number of DG nodes per element and per dimension
    nN = np.array( [ 2, 1, 1 ], dtype = np.int64 )

    ID     = 'DynamicTOV_nN02_nX032' # PlotFileNameRoot
    StepNo = 101

    fileNamePrefix = 'CF_D'

    # END User-defined data

    dataDirectory \
      = rootDir + '{:}.plt{:}_nodal/'.format( ID, str( StepNo ).zfill( 8 ) )

    x1n, un = getData( dataDirectory, fileNamePrefix, nN )

    # Unit conversions

    SpeedOfLightMKS          = 2.99792458e8
    GravitationalConstantMKS = 6.673e-11

    Meter    = 1.0
    Second   = SpeedOfLightMKS * Meter
    Kilogram = GravitationalConstantMKS * Meter**3 / Second**2

    Kilometer  = 1.0e3  * Meter
    Centimeter = 1.0e-2 * Meter

    Gram = 1.0e-3 * Kilogram

    MassDensityUnit = Gram / Centimeter**3

    # Plot nodal data

    import matplotlib.pyplot as plt

    plt.plot( x1n / Kilometer, un / MassDensityUnit, 'k.' )
    plt.show()

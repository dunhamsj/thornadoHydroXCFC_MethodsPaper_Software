#!/usr/bin/env python3

from datetime import datetime
import os
import numpy as np

import GlobalVariables.Settings as gvS
gvS.PlotDirectory = '../../thornadoHydroXCFC_MethodsPaper_Data/'
gvS.Verbose = True
from GlobalVariables.Units   import SetSpaceTimeUnits

from Utilities.Files         import GetFileNumberArray
from Utilities.MakeDataArray import MakeProbelmDataDirectory

def getDensityDecades( suffix ):

    ID = 'AdiabaticCollapse_XCFC'
    idSuffix = ''

    plotfileDirectory \
      = gvS.PlotDirectory \
          + 'AdiabaticCollapse_XCFC{:}/'.format( suffix )

    ID += idSuffix

    plotfileBaseName = ID + '.plt'

    dataDirectory = '.{:}{:}/'.format( ID, suffix )

    SSi = -1
    SSf = -1
    nSS = -1

    SetSpaceTimeUnits( 'spherical', True )

    plotfileArray \
      = GetFileNumberArray \
          ( plotfileDirectory,\
            plotfileBaseName,\
            SSi, SSf, \
            1 )

    MakeProbelmDataDirectory( plotfileArray, \
                              plotfileDirectory,   \
                              plotfileBaseName,    \
                              'PF_D',      \
                              dataDirectory,   \
                              'AMReX'     )

    if SSi == -1: SSi = 0
    if SSf == -1: SSf = plotfileArray.shape[0]-1
    if nSS == -1: nSS = plotfileArray.shape[0]

    densityDecades = np.logspace( 10, 14, 5 )
    nDecades = densityDecades.shape[0]

    foundDecade = [ False for iDecade in range( nDecades ) ]
    foundDecade = np.array( foundDecade, bool )

    ind = np.empty( (nDecades), np.int64   )
    t   = np.empty( (nDecades), np.float64 )

    SS = np.linspace( SSi, SSf, nSS, dtype = np.int64 )

    density = 0.0
    rhob    = 0.0
    tb      = 0.0
    indb    = 0

    for iSS in range( nSS ):

        if iSS % 10 == 0:
          print( '\r  {:}/{:}'.format( iSS, nSS ), end = '\r' )

        fileDirectory = dataDirectory + str( plotfileArray[SS[iSS]] ) + '/'

        timeFile = fileDirectory + '{:}.dat'.format( 'Time' )
        dataFile = fileDirectory + '{:}.dat'.format( 'PF_D'  )

        data = np.loadtxt( dataFile )
        time = np.loadtxt( timeFile )

        density = data[0]

        if density > rhob:

            rhob = density
            tb   = time
            indb = SS[iSS]

            for iDecade in range( nDecades ):

                if density > densityDecades[iDecade] and not foundDecade[iDecade]:

                    X1File = fileDirectory + '{:}.dat'.format( 'X1'   )
                    X1_C   = np.loadtxt( X1File   )

                    foundDecade[iDecade] = True
                    ind        [iDecade] = SS[iSS]
                    t          [iDecade] = time

    print()

    filename = 'processedData/DensityDecades{:}.dat'.format( suffix )
    with open( filename, 'w' ) as f:

        f.write( 'Generated by {:}\non {:}\n' \
             .format( __file__, datetime.today() ) )

        f.write( 'indb = {:d}\n'.format( indb ) )

        f.write( 'tb = t[indb] = {:.3e} ms\n'.format( tb ) )

        f.write( 'rhob = rho[indb] = {:.3e} g/cm^3\n'.format( rhob ) )

        f.write( 't - tb [ms] = np.array( [ ' )

        for iDec in range( nDecades-1 ):
            f.write( '{:.3e}, '.format( np.float64( t[iDec]-tb ) ) )
        f.write( '{:.3e} ], dtype = np.float64 )\n' \
                 .format( np.float64( t[nDecades-1]-tb ) ) )

        f.write( 'snapshots = np.array( [ ' )
        for i in range( ind.shape[0]-1 ):
            f.write( '{:d}, '.format( np.int64( ind[i] ) ) )
        f.write( '{:d} ], dtype = np.int64 )' \
                 .format( np.int64( ind[ind.shape[0]-1] ) ) )

    print( '\n  Generated {:}'.format( filename ) )

if __name__ == '__main__':

#    suffix = '_AMR_dr0.25km'
#    suffix = '_AMR_dr0.50km'
#    suffix = '_AMR_dr1.00km'
#    suffix = '_Uni_dr0.50km'
    suffix = '_Uni_dr1.00km'

    getDensityDecades( suffix )

    import os
    os.system( 'rm -rf __pycache__' )
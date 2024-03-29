#!/usr/bin/env python3

from datetime import datetime
import numpy as np

import GlobalVariables.Settings as gvS
gvS.PlotDirectory = '../../thornadoHydroXCFC_MethodsPaper_Data/'

from Utilities.Files        import GetFileNumberArray
from Utilities.GetFrameData import GetFrameData

ID = 'AdiabaticCollapse_XCFC'

plotfileBaseName = ID + '.plt'

suffix = [ '_Uni_dr0.50km', '_AMR_dr0.50km' ]

# These come from processedData/ShockRadii<suffix>.dat
snapshots = [ np.array( [ 2432, 2504, 2622, 2923, 3623, 4940 ], dtype = np.int64 ), \
              np.array( [ 2018, 2088, 2201, 2494, 3170, 4444 ], dtype = np.int64 ) ]

Fields = [ 'PF_D', 'AF_T', 'AF_Ye', 'AF_S' ]

print( '\n Generating data...' )

for s in range( len( suffix ) ) :

    plotfileDirectory \
      = gvS.PlotDirectory \
          + '{:}{:}/'.format( ID, suffix[s] )

    plotfileArray \
      = GetFileNumberArray \
          ( plotfileDirectory,\
            plotfileBaseName,\
            -1, -1, \
            1 )

    print( '\n    {:}'.format( suffix[s][1:] ) )

    for iSS in range( snapshots[s].shape[0] ):

        ss = str( plotfileArray[snapshots[s][iSS]] ).zfill( 8 )

        print( '      {:}'.format( ss ) )

        for i in range( len( Fields ) ):

            Data, DataUnit, X1, X2, X3, dX1, dX2, dX3, Time \
              = GetFrameData \
                  ( plotfileDirectory \
                      + '{:}{:}'.format( plotfileBaseName, ss ), \
                                         'AMReX', Fields[i], \
                    SaveTime = True )
            filename \
               = 'processedData/{:}_{:}_{:}.dat' \
                  .format( suffix[s][1:], Fields[i], ss )
            header \
              = 'Generated by {:}\non {:}\nr [km], {:} {:}' \
                .format( __file__, datetime.today(), Fields[i], DataUnit )
            np.savetxt( filename, \
                        np.vstack( ( X1, Data ) ), header = header )
            print( '        Saved {:}'.format( filename ) )

import os
os.system( 'rm -rf __pycache__ ' )

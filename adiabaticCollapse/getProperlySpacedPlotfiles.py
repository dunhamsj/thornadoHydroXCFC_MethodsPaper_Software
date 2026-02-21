#!/usr/bin/env python

'''
Because of restarting from checkpoints, not all plotfiles are separated
by the same time increment.
This script creates soft links of the entries in
`${PWD}/../../thornadoHydroXCFC_MethodsPaper_Data/adiabaticCollapse/processedData/validPlotfiles<suffix>`
that are separated from each other by at least 0.05 ms
and puts them in `plotfileDirectory`

NOTE: Only execute this if you've already run `getValidPlotfiles.sh`
      on the full collection of plotfiles
'''

import numpy as np
import os

import globalVariables as gv

plotfileDirectoryRoot \
  = gv.dataDirectory + 'adiabaticCollapse/'

def doit( suffix ):

    print( '\n  Getting properly-spaced plotfiles for: {:}' \
           .format( suffix[1:] ) )
    print(   '  --------------------------------------' )

    infile \
      = plotfileDirectoryRoot \
          + 'processedData/validPlotfiles{:}.dat'.format( suffix )

    if ( not os.path.isfile( infile ) ) :
        msg  = '  >>> File {:} does not exist.\n'.format( infile )
        msg += '  >>> Please execute `getValidPlotfiles.sh` for dataset {:}.\n' \
               .format( suffix[1:] )
        exit( msg + '  >>> Exiting.' )

    lnDir = plotfileDirectoryRoot + 'AdiabaticCollapse_XCFC{:}/'.format( suffix )
    if ( not os.path.isdir( lnDir ) ) :
        os.system( 'mkdir -p {:}'.format( lnDir ) )

    allfiles = []
    alltimes = []
    with open( infile, 'r' ) as f:
        for file in f.readlines():
            if ( '#' in file ) : continue
            x = file.split( ' ' )
            allfiles.append( x[0] )
            alltimes.append( np.float64( x[1] ) )

    times = [alltimes[0]]
    files = [allfiles[0]]
    j = 0
    for i in range( 1, len( alltimes )-1 ):
        if alltimes[i] - times[j] > 0.05:
            times.append( alltimes[i] )
            files.append( allfiles[i] )
            j += 1

    print( '    Number of valid plotfiles:           ', len( allfiles ) )
    print( '    Number of properly-spaced plotfiles: ', len( files ) )

    for i in range( len( files ) ):
        print( '\r    {:}/{:}'.format( i+1, len(files) ), end = '\r' )
        cpstr = 'ln -sf {:} {:}'.format( files[i], lnDir )
        os.system( cpstr )
    print()

doit( '_AMR_dr0.25km' )
doit( '_AMR_dr0.50km' )
doit( '_AMR_dr1.00km' )
doit( '_Uni_dr0.50km' )
doit( '_Uni_dr1.00km' )
doit( '_AMR_dr0.25km_nLevels04' )
doit( '_AMR_dr0.25km_HLLC' )

os.system( 'rm -rf __pycache__' )

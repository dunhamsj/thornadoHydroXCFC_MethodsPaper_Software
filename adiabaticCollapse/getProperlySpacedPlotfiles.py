#!/usr/bin/env python3

'''
Because of restarting from checkpoints, not all plotfiles are separated
by the same time increment.
This script creates soft links of the entries in
`${PWD}/processedData/validPlotfiles<suffix>`
that are separated from each other by at least 0.9 ms
and puts them in `gvS.PlotDirectory`
'''

import numpy as np
import os

import GlobalVariables.Settings as gvS
gvS.PlotDirectory = '../../thornadoHydroXCFC_MethodsPaper_Data/'

#suffix = '_AMR_dr0.25km'
#suffix = '_AMR_dr0.50km'
suffix = '_AMR_dr1.00km'
#suffix = '_Uni_dr0.50km'
#suffix = '_Uni_dr1.00km'

pltDir \
  = '/lump/data/adiabaticCollapse_XCFC/AdiabaticCollapse_XCFC{:}_all' \
    .format( suffix )
lnDir = gvS.PlotDirectory + 'AdiabaticCollapse_XCFC{:}/'.format( suffix )

outfile = 'processedData/validPlotfiles{:}.dat'.format( suffix )

allfiles = []
alltimes = []
with open( outfile, 'r' ) as f:
    for file in f.readlines():
        if ( '#' in file ) : continue
        x = file.split( ' ' )
        allfiles.append( x[0] )
        alltimes.append( np.float64( x[1] ) )

times = [alltimes[0]]
files = [allfiles[0]]
j = 0
for i in range( 1, len( alltimes )-1 ):
    if alltimes[i] - times[j] > 0.09:
        times.append( alltimes[i] )
        files.append( allfiles[i] )
        j += 1

print( 'Number of valid plotfiles:           ', len( allfiles ) )
print( 'Number of properly-spaced plotfiles: ', len( files ) )

for i in range( len( files ) ):
    print( '\r {:}/{:}'.format( i+1, len(files) ), end = '\r' )
    cpstr = 'ln -sf {:} {:}'.format( files[i], lnDir )
    os.system( cpstr )
print()

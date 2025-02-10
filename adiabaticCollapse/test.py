#!/usr/bin/env python3

from myUtilitiesModule import readDensityDecadesFile, readShockRadiusSnapshotsFile

import globalVariables as gv

filename = gv.dataDirectory + 'adiabaticCollapse/processedData/DensityDecades_AMR_dr0.25km_HLLC.dat'
readDensityDecadesFile( filename )

filename = gv.dataDirectory + 'adiabaticCollapse/processedData/ShockRadiusSnapshots_AMR_dr0.25km_HLLC.dat'
readShockRadiusSnapshotsFile( filename )

#!/usr/bin/env python3

from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
plt.style.use( '../publication.sty' )

import globalVariables as gv

from myUtilitiesModule import readShockRadiusSnapshotsFile

saveFig = False
figName \
  = gv.paperDirectory + 'Figures/fig.ShockTrajectory.pdf'
figName = 'fig.ShockTrajectory.png'

dataDirectory = gv.dataDirectory + 'adiabaticCollapse/processedData/'

suffix = [ \
'_AMR_dr0.25km', \
'_AMR_dr0.50km', \
'_AMR_dr1.00km', \
'_Uni_dr0.50km', \
'_Uni_dr1.00km', \
'_AMR_dr0.25km_nLevels04', \
'_AMR_dr0.25km_HLLC' \
]

N = len( suffix )

tArr   = np.empty( N, object )
RshArr = np.empty( N, object )
VshArr = np.empty( N, object )

for s in range( N ):

    filename = dataDirectory + 'ShockRadiusSnapshots{:}.dat'.format( suffix[s] )
    snapshots, tmtb, Rsh = readShockRadiusSnapshotsFile( filename )

    Vsh = []
    iOS = 2
    for i in range( iOS ):
        Vsh.append( 1.0 )
    for i in range( iOS, Rsh.shape[0]-iOS ):
      v = Rsh[i+iOS] - Rsh[i]
      Vsh.append( v )
    for i in range( iOS ):
        Vsh.append( 1.0 )

    VshArr[s] = np.array( Vsh )

    tArr  [s] = tmtb
    RshArr[s] = Rsh

fig, ax = plt.subplots( 1, 1 )

color = gv.color
c = [ color[2], color[0], color[1], color[0], color[1] ]
c = color
for s in range( N ):

    try:
        ind = np.where( VshArr[s] < -1.0e3 )[0][0]
    except:
        ind = -1
    print( suffix[s][1:], ind, tArr[s][ind] )

    if ( 'AMR' in suffix[s] ) :
        ls = '-'
    else:
        ls = '--'

    ax.plot( tArr[s][:ind], RshArr[s][:ind], c = c[s], ls = ls, label = suffix[s][1:] )

ax.legend( loc = 2 )
ax.set_xlabel( r'$t-t_{\mathrm{b}}\ \left[\mathrm{ms}\right]$' )
ax.set_ylabel( r'$R_{\mathrm{sh}}\ \left[\mathrm{km}\right]$' )

if ( saveFig ) :
    plt.savefig( figName, dpi = 300 )
    print( '\n  Saved {:}'.format( figName ) )
else :
    plt.show()

import os
os.system( 'rm -rf __pycache__' )

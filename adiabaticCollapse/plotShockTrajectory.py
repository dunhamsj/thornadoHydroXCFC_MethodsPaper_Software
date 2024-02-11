#!/usr/bin/env python3

from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
plt.style.use( '../publication.sty' )

import GlobalVariables.Settings as gvS
gvS.PlotDirectory = '../../thornadoHydroXCFC_MethodsPaper_Data/'

suffix = [ '_AMR_dr0.25km', '_AMR_dr0.50km', '_AMR_dr1.00km', '_Uni_dr0.50km', '_Uni_dr1.00km' ]
suffix = [ '_AMR_dr0.25km', '_AMR_dr1.00km', '_Uni_dr0.50km', '_Uni_dr1.00km' ]

N = len( suffix )

tArr   = np.empty( N, object )
RshArr = np.empty( N, object )
VshArr = np.empty( N, object )

for s in range( N ):

    filename  = 'processedData/ShockRadiusVsTime{:}.dat'.format( suffix[s] )
    t, ss, Rsh = np.loadtxt( filename )

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

    tArr  [s] = t
    RshArr[s] = Rsh

fig, ax = plt.subplots( 2, 1 )

for s in range( N ):

    ind = np.where( VshArr[s] < -1.0e3 )[0][0]
    ind = -1
    ax[0].plot( tArr[s][:ind], RshArr[s][:ind], '.', label = suffix[s][1:] )
    ax[1].plot( tArr[s], VshArr[s], '.' )

ax[0].legend( loc = 1 )
fig.supxlabel( r'$t-t_{\mathrm{b}}\ \left[\mathrm{ms}\right]$' )
ax[0].set_ylabel( r'$R_{\mathrm{sh}}\left(t\right)\ \left[\mathrm{km}\right]$' )
ax[1].set_ylabel( r'$R_{\mathrm{sh}}\left(t+\Delta t\right)-R_{\mathrm{sh}}\left(t\right)\ \left[\mathrm{km}\right]$' )

plot = False
if ( plot ) :
    plt.show()
else:
    figName \
      = '/home/kkadoogan/Work/thornadoHydroXCFC_MethodsPaper/\
    Figures/fig.ShockTrajectory_dr0.50km.pdf'
    figName = '/home/kkadoogan/fig.png'
    plt.savefig( figName, dpi = 300 )
    print( '\n  Saved {:}'.format( figName ) )

import os
os.system( 'rm -rf __pycache__' )

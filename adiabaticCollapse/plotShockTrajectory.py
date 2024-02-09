#!/usr/bin/env python3

from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
plt.style.use( '../publication.sty' )

import GlobalVariables.Settings as gvS
gvS.PlotDirectory = '../../thornadoHydroXCFC_MethodsPaper_Data/'

tb = 241.7

suffix = [ '_Uni_dr0.50km', '_AMR_dr0.50km' ]

fig, axs = plt.subplots( 2, 1 )

xSh = [ 1.0e2, 5.0e2, 1.0e3, 2.0e3, 4.0e3, 7.5e3 ]
for s in range( len( suffix ) ):

    filename  = 'ShockRadiusVsTime{:}.dat'.format( suffix[s] )
    t, ss, Rsh = np.loadtxt( filename )

    ind = np.where( ( t < 267 ) )[0]
    ind2 = np.where( ( t[:-1] < 267 ) )[0]

    t   = np.copy( t  [ind] )
    Rsh = np.copy( Rsh[ind] )

    Vsh = []

    ii = 1
    t2  = []
    Vsh = []
    for i in range( ii, Rsh.shape[0]-ii ):
      v = ( Rsh[i+ii] - Rsh[i] ) / ( ii * ( t[i+ii] - t[i] ) )
      t2.append( t[i] )
      Vsh.append( v )

    axs[0].plot( t[ind], Rsh[ind], label = suffix[s][1:] )
    axs[1].plot( t2, Vsh, '.' )

for i in xSh:
    axs[0].axhline( i, color = 'k' )

axs[0].legend()

fig.supxlabel( 't-tb [ms]' )

axs[0].set_ylabel( 'Rsh [km]' )

plot = True
if ( plot ) :
    plt.show()
else:
    figName \
      = '/home/kkadoogan/Work/thornadoHydroXCFC_MethodsPaper/\
    Figures/fig.ShockTrajectory_dr0.50km.pdf'
    plt.savefig( figName, dpi = 300 )
    print( '\n  Saved {:}'.format( figName ) )

import os
os.system( 'rm -rf __pycache__' )

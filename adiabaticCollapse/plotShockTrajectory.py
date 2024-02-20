#!/usr/bin/env python3

from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
plt.style.use( '../publication.sty' )

import GlobalVariables.Settings as gvS
gvS.PlotDirectory = '../../thornadoHydroXCFC_MethodsPaper_Data/'

suffix = [ '_AMR_dr0.25km', '_AMR_dr0.50km', '_AMR_dr1.00km', '_Uni_dr0.50km', '_Uni_dr1.00km' ]
#suffix = [ '_AMR_dr0.50km', '_AMR_dr1.00km', '_Uni_dr0.50km', '_Uni_dr1.00km' ]

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

fig, ax = plt.subplots( 1, 1 )

# colorblind-friendly palette: https://gist.github.com/thriveth/8560036
color = ['#377eb8', '#ff7f00', '#4daf4a', \
         '#f781bf', '#a65628', '#984ea3', \
         '#999999', '#e41a1c', '#dede00']

c = [ color[2], color[0], color[1], color[0], color[1] ]
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

#    ax.plot( tArr[s][:ind], RshArr[s][:ind], c = c[s], ls = ls, label = suffix[s][1:] )

exit()
ax.legend( loc = 2 )
ax.set_xlabel( r'$t-t_{\mathrm{b}}\ \left[\mathrm{ms}\right]$' )
ax.set_ylabel( r'$R_{\mathrm{sh}}\ \left[\mathrm{km}\right]$' )

plot = False
if ( plot ) :
    plt.show()
else:
    figName \
      = '/home/kkadoogan/Work/thornadoHydroXCFC_MethodsPaper/\
    Figures/fig.ShockTrajectory.pdf'
    figName = '/home/kkadoogan/fig.ShockTrajectory.png'
    plt.savefig( figName, dpi = 300 )
    print( '\n  Saved {:}'.format( figName ) )

import os
os.system( 'rm -rf __pycache__' )

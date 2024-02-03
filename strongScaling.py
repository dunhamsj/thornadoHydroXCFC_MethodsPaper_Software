#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
plt.style.use( 'publication.sty' )

import GlobalVariables.Settings as gvS

nprocs, wtimes \
  = np.loadtxt( gvS.PlotDirectory + 'StrongScaling/walltimes.dat', \
                unpack = True )

nDOF = [ np.int64( 256 * 512 * 6 * 9 / i ) for i in nprocs ]

wtimes /= wtimes[0]

fig, ax = plt.subplots( 1, 1, figsize = (8,2) )

ax.grid( which = 'both' )

ax.plot( nprocs, wtimes            , '.', label = 'Acutal Scaling' )
ax.plot( nprocs, 0.8 * 1.0 / nprocs, '-', label = 'Ideal Scaling'  )

for i in range( len( nDOF ) ):
    ax.text( 0.9 * nprocs[i], 2e-2, '{:.0e}'.format( nDOF[i] ) )

ax.legend()

ax.set_xscale( 'log' )
ax.set_yscale( 'log' )

ax.set_xlabel( 'nProc' )
ax.set_ylabel( r'$t\left(\mathrm{nProc}\right)/t\left(1\right)$' )

#plt.show()

figName \
  = '/home/kkadoogan/Work/thornadoHydroXCFC_MethodsPaper/\
Figures/fig.StrongScaling.pdf'
plt.savefig( figName, dpi = 300 )
print( '\n  Saved {:}'.format( figName ) )

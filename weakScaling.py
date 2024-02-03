#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
plt.style.use( 'publication.sty' )

import GlobalVariables.Settings as gvS

nprocs, wtimes \
  = np.loadtxt( gvS.PlotDirectory + 'WeakScaling/walltimes.dat', \
                unpack = True )

wtimes /= 20. # Number of cycles

fig, ax = plt.subplots( 1, 1, figsize = (8,2) )

ax.grid( which = 'both' )

ax.plot( nprocs, wtimes, '.' )

ax.set_xscale( 'log' )
#ax.set_yscale( 'log' )

ax.set_xlabel( 'nProc' )
ax.set_ylabel( r'$\mathrm{Walltime\ per\ timestep\ [s]}$' )

#plt.show()

figName \
  = '/home/kkadoogan/Work/thornadoHydroXCFC_MethodsPaper/\
Figures/fig.WeakScaling.pdf'
plt.savefig( figName, dpi = 300 )
print( '\n  Saved {:}'.format( figName ) )

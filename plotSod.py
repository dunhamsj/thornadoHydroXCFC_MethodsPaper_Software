#!/usr/bin/env python3

import numpy as np
from sys import argv
import matplotlib.pyplot as plt
plt.style.use( 'publication.sty' )

import GlobalVariables.Settings as gvS
gvS.PlotDirectory = '../thornadoHydroXCFC_MethodsPaper_Data/'
import GlobalVariables.Units    as gvU

from Utilities.GetPlotData              import GetPlotData
from Utilities.RefinementBoundaryFinder import FindRefinementBoundaries

#### ========== User Input ==========

DataType = 'AMReX'

# Specify name of problem
ProblemName = [ 'RiemannProblem1D_Sod_nX0256', \
                'RiemannProblem1D_Sod_nX0016_AMR' ]

rootDir = '/home/kkadoogan/Work/Analysis/thornadoHydroXCFC_MethodsPaper_Data/Sod/'
# Specify directory containing amrex Plotfiles
PlotDirectory = rootDir

# Specify plot file base name
PlotBaseName = [ i + '.plt' for i in ProblemName ]

xLabel = r'$x$'
yLabel = [ r'$\rho$', r'$v$', r'$p$' ]

# Specify to plot in log-scale
UseLogScale_X  = False
UseLogScale_Y  = False

# Specify whether or not to use physical units
UsePhysicalUnits = False

# Specify coordinate system (currently supports 'cartesian' and 'spherical')
CoordinateSystem = 'cartesian'

# Max level of refinement to plot (-1 plots leaf elements)
MaxLevel = -1

# Write extra info to screen
Verbose = False

# Use custom limts for y-axis
UseCustomLimits = False
vmin = 0.0
vmax = 2.0

ShowRefinement = False

# Save figure (True) or plot figure (False)
SaveFig = True

#### ====== End of User Input =======

#FigName = 'fig.Sod.png'
FigName = '/home/kkadoogan/Work/thornadoHydroXCFC_MethodsPaper/Figures/fig.Sod.pdf'

# Append "/" to PlotDirectory, if not present
if not PlotDirectory[-1] == '/': PlotDirectory += '/'

gvU.SetSpaceTimeUnits( CoordinateSystem, UsePhysicalUnits )

xL = 0.0
xH = 1.0

eps = 0.05
xLim = [ xL - eps, xH + eps ]

xE, pE, rhoE, vE, eE \
  = np.loadtxt( rootDir + 'sod.dat', unpack = True, skiprows = 1 )

fig, axs = plt.subplots( 3, 1, figsize = (8,4) )

lw = 1.0
ms = 2.0
labels = [ 'Exact', r'$N_{K}=256$', 'AMR' ]
axs[0].plot( xE, rhoE, 'k-', lw = lw, label = labels[0] )
axs[1].plot( xE, vE  , 'k-', lw = lw )
axs[2].plot( xE, pE  , 'k-', lw = lw )

for i in range( len( PlotBaseName ) ):

    rho, DataUnit, Time, X1_C, X2_C, X3_C, dX1, dX2, dX3 \
      = GetPlotData \
          ( PlotDirectory     , \
            PlotBaseName[i]   , \
            'PF_D'            , \
            argv = argv       , \
            DataType = 'AMReX', \
            Verbose = Verbose )

    v  , DataUnit, Time, X1_C, X2_C, X3_C, dX1, dX2, dX3 \
      = GetPlotData \
          ( PlotDirectory     , \
            PlotBaseName[i]   , \
            'PF_V1'           , \
            argv = argv       , \
            DataType = 'AMReX', \
            Verbose = Verbose )

    p  , DataUnit, Time, X1_C, X2_C, X3_C, dX1, dX2, dX3 \
      = GetPlotData \
          ( PlotDirectory     , \
            PlotBaseName[i]   , \
            'AF_P'            , \
            argv = argv       , \
            DataType = 'AMReX', \
            Verbose = Verbose )

    axs[0].plot( X1_C, rho, '.', markersize = ms, label = labels[i+1] )
    axs[1].plot( X1_C, v  , '.', markersize = ms )
    axs[2].plot( X1_C, p  , '.', markersize = ms )

    #if ( ShowRefinement ) :

    #    nX1 = X1_C.shape[0]
    #    x = xL
    #    for i in range( nX1 ):
    #        x += dX1[i]
    #        ax.axvline( x )

axs[0].legend()
fig.supxlabel( xLabel, fontsize = 15 )
for i in range( axs.shape[0] ):
    axs[i].set_xlim( xLim )
    axs[i].set_ylabel( yLabel[i], fontsize = 15 )
    axs[i].grid()
    if ( i < axs.shape[0]-1 ) :
        axs[i].set_xticklabels( '' )

if UseCustomLimits: ax.set_ylim( vmin, vmax )

plt.subplots_adjust( hspace = 0.0 )

if SaveFig:

    plt.savefig( FigName, dpi = 300 )
    print( '\n  Saved {:}'.format( FigName ) )

else:

    plt.show()

plt.close()

import os
os.system( 'rm -rf __pycache__ ' )

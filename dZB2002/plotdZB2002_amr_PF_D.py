#!/usr/bin/env python3

import numpy as np
import yt

import globalVariables as gv

from myUtilitiesModule import getPlotfileNumberArray

### Beginning of user input ###

# Specify name of problem

problemName = 'RiemannProblem2D_dZB2002_amr'
figTitle = 'AMR'

field = 'PF_D'
label = r'$\rho$'
zmin = 0.1
zmax = 2
cmap = 'viridis'

suffix = 'pdf'

#figName = gv.paperDirectory + 'Figures/\
#fig.dZB2002_amr.{:}'.format( suffix )
figName = 'fig.dZB2002_amr_{:}.{:}'.format(field, suffix)

dataDirectory = gv.dataDirectory + 'dZB2002/'
#dataDirectory ='/mnt/shared/work/codes/thornado/SandBox/AMReX/\
#dgExperiments_Euler_Relativistic_IDEAL/rp2d_amr/' 
##dgExperiments_Euler_Relativistic_IDEAL/rp2d_uni/'

# Specify plot file base name
plotfileNameRoot = problemName + '.plt.'

fileNumberArray \
  = getPlotfileNumberArray(dataDirectory, plotfileNameRoot)
print(fileNumberArray)

ds = yt.load(dataDirectory + plotfileNameRoot \
               + str(fileNumberArray[-1]).zfill(8))

bl = 'boxlib'
blField = (bl,field)

slc \
  = yt.SlicePlot \
      (ds, 'z', blField, origin = 'native')

slc.set_cmap(blField, cmap)

slc.set_colorbar_label(field, label)

slc.set_zlim(field, zmin = zmin, zmax = zmax)

slc.set_log(field, log = True)

slc.set_minorticks         (field, True)
slc.set_colorbar_minorticks(field, True)

slc.set_xlabel(r'$x$')
slc.set_ylabel(r'$y$')

slc.annotate_cell_edges(line_width = 1.0e-12, alpha = 0.5, color = 'black')

slc.annotate_text \
  ( (0.13, 0.915), \
    figTitle, \
    coord_system = 'figure', \
    text_args \
      = {'color' : 'black', \
         'size' : 26})

slc.save(figName, suffix = suffix, mpl_kwargs = {'bbox_inches':'tight'})
print('\n  Saved {:}'.format(figName))

import os
os.system('rm -rf __pycache__')

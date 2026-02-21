#!/usr/bin/env python

import numpy as np
import yt

import globalVariables as gv
import matplotlib.pyplot as plt
plt.rcParams.update({'text.usetex': True})

from myUtilitiesModule import getPlotfileNumberArray

problemName = 'RiemannProblem2D_dZB2002_amr'
figTitle = 'AMR'

field = 'PF_D'
label = r'$\rho$'
zmin = 0.01
zmax = 4.0
cmap = 'viridis'

suffix = 'pdf'

figName = gv.paperDirectory + 'Figures/\
fig.dZB2002_amr_mesh.{:}'.format(suffix)

dataDirectory = gv.dataDirectory + 'dZB2002/'

plotfileNameRoot = problemName + '.plt.'

fileNumberArray \
  = getPlotfileNumberArray(dataDirectory, plotfileNameRoot)

ds = yt.load(dataDirectory + plotfileNameRoot \
               + str(fileNumberArray[-1]).zfill(8))

ad = ds.all_data()
data = ad[field].to_ndarray()
print('Number of leaf elements: ', data.shape[0])

bl = 'boxlib'
blField = (bl,field)

slc \
  = yt.SlicePlot \
      (ds, 'z', blField, origin = 'native')

slc.set_cmap(blField, cmap)
slc.set_axes_unit('unitary')

slc.set_zlim(field, zmin = zmin, zmax = zmax)

slc.set_log(field, log = True)

slc.set_minorticks         (field, True)
slc.set_colorbar_minorticks(field, True)

slc.annotate_cell_edges(line_width = 1.0e-12, alpha = 0.5, color = 'black')

slc.annotate_text \
  ( (0.2, 0.815), \
    figTitle, \
    coord_system = 'figure', \
    inset_box_args = dict(facecolor = 'white', edgecolor = 'black', boxstyle = 'round', alpha = 0.8), \
    text_args \
      = {'color' : 'black', \
         'size' : 26})

fig = slc.export_to_mpl_figure((1,1), cbar_pad = '1%')
ax = slc.plots[bl, field].axes
cax = slc.plots[bl, field].cax
cbar = slc.plots[bl, field].cb
cbar.set_label(label, size = 40)
ax.set_xlabel(r'$x$', fontsize = 40)
ax.set_ylabel(r'$y$', fontsize = 40)
ax.tick_params( axis = 'both', labelsize = 28 )
cax.tick_params( labelsize = 28 )

slc.save(figName, suffix = suffix, mpl_kwargs = {'bbox_inches':'tight'})
print('\n  Saved {:}'.format(figName))

import os
os.system('rm -rf __pycache__')

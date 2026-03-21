#!/usr/bin/env python3

import numpy as np
import yt
yt.funcs.mylog.setLevel(40) # Suppress yt warnings
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
plt.style.use('publication.sty')

from myUtilitiesModule import getPlotfileNumberArray
import globalVariables as gv

### Beginning of user input ###

# Specify name of problem
problemName = 'StandingAccretionShock_XCFC'

plotfileDirectory = gv.dataDirectory + 'sasi/'

# Specify plot file base name
plotfileNameRoot = problemName + '.plt'

# Set xlabel and ylabel
xLabel = r'$r\ \left[\mathrm{km}\right]$'
yLabel = r'$z\ \left[\mathrm{km}\right]$'

# Specify field to plot
field = 'PF_D'

# Label for colorbar (z-axis)
zLabel = r'$\rho\ \left[\mathrm{g\,cm}^{-3}\right]$'

figNameRoot = gv.paperDirectory + 'Figures/fig.sasi'

# Colormap for plot
cmap = 'viridis'

# Use log scale for z-axis
useLogScaleZ = True

# Show mesh
ShowMesh  = True
MeshAlpha = 0.05

# Outer boundary of plot
xH = 1.5e2

# Colorbar limits
vmin = 1.0e7
vmax = 3.0e10

SS = [ 0, 1, 3, 2 ]

### End of user input ###

bl = 'boxlib'
blfield = (bl, field)

plotfileNumberArray \
  = getPlotfileNumberArray \
      (plotfileDirectory, \
       plotfileNameRoot)

fig, ax = plt.subplots()
ax.grid(False)
ax.set_xlim([-xH, xH])
ax.set_ylim([-xH, xH])
ax.set_xlabel(xLabel, fontsize = 16)
ax.set_ylabel(yLabel, fontsize = 16)

# Adapted from
# https://stackoverflow.com/questions/28752727/
# map-values-to-colors-in-matplotlib
norm = mpl.colors.LogNorm(vmin = vmin, vmax = vmax, clip = True)
mapper = mpl.cm.ScalarMappable(norm = norm, cmap = cmap)

pe = 1
figName = figNameRoot + '.pdf'
    
for j in range(len(SS)):

    iSS = SS[j]

    ds = yt.load(plotfileDirectory + plotfileNameRoot \
                    + str(plotfileNumberArray[iSS]).zfill(8))
    
    time = np.round(ds.current_time.to_ndarray())

    ad = ds.all_data()
    r      = ad['X1_C'].to_ndarray()
    theta  = ad['X2_C'].to_ndarray()
    dr     = ad['dX1' ].to_ndarray()
    dtheta = ad['dX2' ].to_ndarray()
    d = ad[field].to_ndarray()
    print(d.shape)
    
    if (j == 0):
        ax.text(0.02, 0.94, r'$t = {:.0f}\ \mathrm{{ms}}$'.format(time), \
                fontsize = 12, transform = ax.transAxes)
    if (j == 1):
        ax.text(0.78, 0.94, r'$t = {:.0f}\ \mathrm{{ms}}$'.format(time), \
                fontsize = 12, transform = ax.transAxes)
    if (j == 2):
        ax.text(0.02, 0.04, r'$t = {:.0f}\ \mathrm{{ms}}$'.format(time), \
                fontsize = 12, transform = ax.transAxes)
    if (j == 3):
        ax.text(0.78, 0.04, r'$t = {:.0f}\ \mathrm{{ms}}$'.format(time), \
                fontsize = 12, transform = ax.transAxes)
    
    for i in range(0, d.shape[0], pe):
        if(r[i] + 0.5 * dr[i] > xH): continue

        skip = True

        x = r[i] * np.sin(theta[i])
        z = r[i] * np.cos(theta[i])

        if ((j == 0) | (j == 2)): x *= -1.0

        if((j == 0) & ((z > 0.0) & (x < 0.0))): skip = False
        if((j == 1) & ((z > 0.0) & (x > 0.0))): skip = False
        if((j == 2) & ((z < 0.0) & (x < 0.0))): skip = False
        if((j == 3) & ((z < 0.0) & (x > 0.0))): skip = False

        if (skip): continue

        rL = r[i] - 0.5 * dr[i]
        rH = r[i] + 0.5 * dr[i]
        tL = theta[i] - 0.5 * dtheta[i]
        tH = theta[i] + 0.5 * dtheta[i]

        # Specify corners of polygon
        if ((j == 1) | (j == 3)):
            x11 = rL * np.sin(tL)
            z11 = rL * np.cos(tL)
            x12 = rH * np.sin(tL)
            z12 = rH * np.cos(tL)
            x21 = rH * np.sin(tH)
            z21 = rH * np.cos(tH)
            x22 = rL * np.sin(tH)
            z22 = rL * np.cos(tH)
        else:
            x11 = -rL * np.sin(tL)
            z11 = rL * np.cos(tL)
            x12 = -rH * np.sin(tL)
            z12 = rH * np.cos(tL)
            x21 = -rH * np.sin(tH)
            z21 = rH * np.cos(tH)
            x22 = -rL * np.sin(tH)
            z22 = rL * np.cos(tH)
    
        xy = list(zip([x11, x12, x21, x22], [z11, z12, z21, z22]))
    
        rgba = mapper.to_rgba(d[i])

        ax.add_patch(mpl.patches.Polygon \
                       (xy = xy, fill = True, fc = rgba, ec = rgba))

if (ShowMesh):
    for j in range(len(SS)):

        iSS = SS[j]
    
        ds = yt.load(plotfileDirectory + plotfileNameRoot \
                        + str(plotfileNumberArray[iSS]).zfill(8))
        
        ad = ds.all_data()
        r      = ad['X1_C'].to_ndarray()
        theta  = ad['X2_C'].to_ndarray()
        dr     = ad['dX1' ].to_ndarray()
        dtheta = ad['dX2' ].to_ndarray()
        d = ad[field].to_ndarray()
        
        for i in range(0, d.shape[0], pe):
            if(r[i] > xH): continue

            skip = True

            x = r[i] * np.sin(theta[i])
            z = r[i] * np.cos(theta[i])

            if ((j == 0) | (j == 2)): x *= -1.0

            if((j == 0) & ((z > 0.0) & (x < 0.0))): skip = False
            if((j == 1) & ((z > 0.0) & (x > 0.0))): skip = False
            if((j == 2) & ((z < 0.0) & (x < 0.0))): skip = False
            if((j == 3) & ((z < 0.0) & (x > 0.0))): skip = False

            if (skip): continue

            rL = r[i] - 0.5 * dr[i]
            rH = r[i] + 0.5 * dr[i]
            tL = theta[i] - 0.5 * dtheta[i]
            tH = theta[i] + 0.5 * dtheta[i]

            # Specify corners of polygon
            if ((j == 1) | (j == 3)):
                x11 = rL * np.sin(tL)
                z11 = rL * np.cos(tL)
                x12 = rH * np.sin(tL)
                z12 = rH * np.cos(tL)
                x21 = rH * np.sin(tH)
                z21 = rH * np.cos(tH)
                x22 = rL * np.sin(tH)
                z22 = rL * np.cos(tH)
            else:
                x11 = -rL * np.sin(tL)
                z11 = rL * np.cos(tL)
                x12 = -rH * np.sin(tL)
                z12 = rH * np.cos(tL)
                x21 = -rH * np.sin(tH)
                z21 = rH * np.cos(tH)
                x22 = -rL * np.sin(tH)
                z22 = rL * np.cos(tH)
    
            xy = list(zip([x11, x12, x21, x22], [z11, z12, z21, z22]))

            ax.add_patch(mpl.patches.Polygon \
                           (xy = xy, fill = False, alpha = MeshAlpha))
    
ax.axhline(0.0, lw = 2, c = 'k')
ax.axvline(0.0, lw = 2, c = 'k')
plt.gca().set_aspect('equal')

# Colorbar code from
# https://stackoverflow.com/questions/32462881/add-colorbar-to-existing-axis
divider = make_axes_locatable(ax)
cax = divider.append_axes('top', size = '5%', pad = 0.05)
cb = fig.colorbar(mapper, cax = cax, orientation = 'horizontal')
cb.ax.xaxis.set_ticks_position('top')
cb.ax.xaxis.set_label_position('top')
cb.set_label(r'{:}'.format(zLabel), labelpad = 10.5, fontsize = 16)
plt.savefig(figName, dpi = 300, bbox_inches = 'tight')
print('\n  Saved {:}'.format(figName))
#plt.show()

import os
os.system('rm -rf __pycache__')

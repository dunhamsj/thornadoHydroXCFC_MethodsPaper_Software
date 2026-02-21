#!/usr/bin/env python

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import yt
yt.funcs.mylog.setLevel(40) # Suppress yt warnings

plt.style.use( '../publication.sty' )

import globalVariables as gv

from myUtilitiesModule import getPlotfileNumberArray

### Beginning of user input ###

# Specify name of problem
problemName = 'SedovTaylorBlastWave_Relativistic'

iSS = -1

# Number of elements on coarsest level
nX = 32
nY = 64

nDetCells = '03'

field = 'PF_D'
zlabel = r'$\rho$'

saveFig = True

figName = gv.paperDirectory + 'Figures/fig.stbw_2d.pdf'

# Specify directory containing amrex plotfiles
plotfileDirectoryRoot = gv.dataDirectory
plotfileDirectory = plotfileDirectoryRoot + 'sedovTaylorBlastWave/stbw_2d/'

# Specify plot file base name
plotfileNameRoot = problemName + '.plt'

plotfileNumberArray \
  = getPlotfileNumberArray \
      ( plotfileDirectory,\
        plotfileNameRoot )

plotfileName \
  = plotfileDirectory \
      + '{:}{:}'.format( plotfileNameRoot, \
                         str( plotfileNumberArray[iSS] ).zfill( 8 ) )

ds = yt.load( plotfileName )

# Get lower and higher boundaries and convert them to numpy arrays
xL = ds.domain_left_edge.to_ndarray()
xH = ds.domain_right_edge.to_ndarray()

def interp2d( R, z, f, x, y ):

    indx2 = np.where( x < R )[0][0]
    indx1 = indx2 - 1
    x1 = R[indx1]
    x2 = R[indx2]

    indy2 = np.where( y < z )[0][0]
    indy1 = indy2 - 1
    y1 = z[indy1]
    y2 = z[indy2]

    q11 = f[indx1,indy1]
    q12 = f[indx1,indy2]
    q21 = f[indx2,indy1]
    q22 = f[indx2,indy2]

    fy1 = ( x2 - x ) / ( x2 - x1 ) * q11 + ( x - x1 ) / ( x2 - x1 ) * q21
    fy2 = ( x2 - x ) / ( x2 - x1 ) * q12 + ( x - x1 ) / ( x2 - x1 ) * q22

    return ( y2 - y ) / ( y2 - y1 ) * fy1 + ( y - y1 ) / ( y2 - y1 ) * fy2

data_level_0 \
  = ds.covering_grid( level = 0, left_edge = xL, dims = [ nX, nY, 1 ] )
Rc   = data_level_0['boxlib','X1_C'][:,0,0].to_ndarray()
Zc   = data_level_0['boxlib','X2_C'][0,:,0].to_ndarray()
data = data_level_0['boxlib',field ][:,:,0].to_ndarray()

eps = 1.0e-16
r = np.linspace( Rc.min()+eps, Rc.max()-eps, 100 )
theta = np.linspace( 0.0, np.pi / 2.0, 7 )

y    = np.empty( (r.shape[0],theta.shape[0]), np.float64 )
ybar = np.empty( (r.shape[0]), np.float64 )
for iX2 in range( theta.shape[0] ):

    R = r * np.sin( theta[iX2] )
    Z = r * np.cos( theta[iX2] )

    for iX1 in range( R.shape[0] ):
        y[iX1,iX2] = interp2d( Rc, Zc, data, R[iX1], Z[iX1] )

theta2 = np.linspace( 0.0, np.pi, 100 )

y2 = np.empty( (r.shape[0],theta2.shape[0]), np.float64 )
for iX2 in range( theta2.shape[0] ):

    R = r * np.sin( theta2[iX2] )
    Z = r * np.cos( theta2[iX2] )

    for iX1 in range( R.shape[0] ):
        y2[iX1,iX2] = interp2d( Rc, Zc, data, R[iX1], Z[iX1] )

for iX1 in range( R.shape[0] ):
    ybar[iX1] = 0.5 * np.trapezoid( y2[iX1] * np.sin( theta2 ), \
                                    x = theta2, dx = np.pi / theta2.shape[0] )

fig, axs = plt.subplots( 2, 1 )
for iX2 in range( theta.shape[0] ):
    axs[0].plot( r, y[:,iX2], \
                label = r'$\theta/\pi = {:.3f}$'.format( theta[iX2] / np.pi ) )
    axs[1].plot( r, ( y[:,iX2] - ybar ) / ybar )

data = np.loadtxt( 'spherical_standard_omega0p00_nDetCells{:}_t500.dat' \
                   .format( nDetCells ), skiprows = 2 )
axs[0].plot( data[:,1], data[:,2], 'k-', label = r'Exact' )

xlim = [ -0.1, 1.1 ]
axs[0].set_xlim( xlim )
axs[1].set_xlim( xlim )
fig.supxlabel( r'$R$', y = 0.07 )
axs[0].set_ylabel( r'$\rho$' )
axs[1].set_ylabel( r'$\left( \rho - \left<\rho\right>_{S^{2}} \right) / \left<\rho\right>_{S^{2}}$' )
axs[0].grid()
axs[1].grid()
axs[0].legend()
axs[0].xaxis.set_ticklabels( '' )
plt.subplots_adjust( hspace = 0.0 )
if ( saveFig ) :
    figName2 = 'fig.stbw_2d_symmetry.pdf'
    plt.savefig( figName2, dpi = 300 )
    print( '\n  Saved {:}'.format( figName2 ) )
else:
    plt.show()
plt.close()

# Set xlabel and ylabel
xlabel = r'$R$'
ylabel = r'$z$'

# Colormap for plot
cmap = 'viridis'

# Use custom limits for colorbar
useCustomZmin = False ; zmin = 1.0e-1
useCustomZmax = False ; zmax = 5.0e1

# Use log scale for z-axis
useLogScaleZ = True

# Show mesh
showMesh  = True
meshAlpha = 0.2

### End of user input ###

bl = 'boxlib'
blField = (bl,field)

ad = ds.all_data()
r  = ad['X1_C'].to_ndarray()
z  = ad['X2_C'].to_ndarray()
dr = ad['dX1' ].to_ndarray()
dz = ad['dX2' ].to_ndarray()
d  = ad[field].to_ndarray()
#d -= d.mean()

if ( useLogScaleZ ) :
    d = np.log10( d )

fig, ax = plt.subplots()

# Adapted from
# https://stackoverflow.com/questions/28752727/
# map-values-to-colors-in-matplotlib
if ( d.min() == d.max() ) :
    offset = 0.1
else:
    offset = 0.0
vmin = d.min() - offset
vmax = d.max() + offset
norm = mpl.colors.Normalize( vmin = vmin, vmax = vmax, clip = True )
mapper = mpl.cm.ScalarMappable( norm = norm, cmap = cmap )
for i in range( d.shape[0] ):
    rgba = mapper.to_rgba( d[i] )
    rect = plt.Rectangle( [r[i]-0.5*dr[i],z[i]-0.5*dz[i]], dr[i], dz[i], \
                          ec = None, fc = rgba )
    ax.add_patch( rect )

    if ( showMesh ) :

        rect = plt.Rectangle( [r[i]-0.5*dr[i],z[i]-0.5*dz[i]], dr[i], dz[i], \
                              ec = 'k', lw = 0.5, alpha = meshAlpha )
        rect.set_fill( False )
        ax.add_patch( rect )

plt.gca().set_aspect( 'equal' )
ax.set_xlim( xL[0], xH[0] )
ax.set_ylim( xL[1], xH[1] )
ax.set_xlabel( xlabel )
ax.set_ylabel( ylabel )

# Colorbar code from
# https://stackoverflow.com/questions/32462881/add-colorbar-to-existing-axis
divider = make_axes_locatable( ax )
cax = divider.append_axes( 'right', size = '5%', pad = 0.05 )
if ( useLogScaleZ ) :
    fig.colorbar( mapper, cax = cax, label = r'$\log_{{10}}\,${:}'.format( zlabel ) )
else:
    fig.colorbar( mapper, cax = cax, label = r'{:}'.format( zlabel ) )
    #fig.colorbar( mapper, cax = cax, label = r'{:}$-\bar{{\rho}}$'.format( zlabel ) )

if ( saveFig ) :
    plt.savefig( figName, dpi = 300 )
    print( '\n  Saved {:}'.format( figName ) )
else:
    plt.show()

import os
os.system( 'rm -rf __pycache__ ' )

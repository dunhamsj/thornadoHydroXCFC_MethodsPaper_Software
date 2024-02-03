#!/usr/bin/env python3

import numpy as np
import yt

import GlobalVariables.Settings as gvS

from Utilities.Files import GetFileNumberArray

### Beginning of user input ###

# Specify name of problem
#ProblemName = 'RiemannProblem2D_dZB2002_032x032'; PlotTitle = '32 x 32'
ProblemName = 'RiemannProblem2D_dZB2002_128x128'; PlotTitle = '128 x 128'
#ProblemName = 'RiemannProblem2D_dZB2002_032x032_AMR'; PlotTitle = 'AMR'

PlotDirectory = gvS.PlotDirectory + 'dZB2002/{:}/'.format( ProblemName )

# Specify plot file base name
PlotBaseName = ProblemName + '.plt'

FileNumberArray \
  = GetFileNumberArray \
      ( PlotDirectory, \
        PlotBaseName, \
        -1, -1, \
        1 )

ds = yt.load( PlotDirectory + PlotBaseName + str( FileNumberArray[-1] ).zfill( 8 ) )

# Get lower and higher boundaries and convert them to numpy arrays
xL = ds.domain_left_edge.to_ndarray()
xH = ds.domain_right_edge.to_ndarray()

# Units for axes (dimensionless -> code_length)
LengthUnitX = [ 'code_length', 'code_length' ]

# Set xlabel and ylabel
xLabel = r'$x$'
yLabel = r'$y$'

# Set center and width of plot window
center = 0.5 * ( xL + xH )
width  = 1.0 * ( xH - xL )

# Zoom in?
Zoom = 1.0

# Specify field to plot
Field = 'AF_P'

# Label for colorbar (z-axis)
zLabel = r'$p$'

# Colormap for plot
cmap = 'Purples'

# Use custom limits for colorbar
UseCustomZmin = True ; zmin = 0.01
UseCustomZmax = True ; zmax = 5.0e1

# Use log scale for z-axis
UseLogScaleZ = True

# Include minor tickmarks (x,Y)
ShowMinorTicksXY = True

# Include minor tickmarks (Z)
ShowMinorTicksZ = True

# Show mesh
ShowMesh  = True
MeshAlpha = 0.5

# Overplot contours
OverplotContours = False
nLevels = 5

### End of user input ###

bl = 'boxlib'
blField = (bl,Field)

slc \
  = yt.SlicePlot \
      ( ds, 'z', blField, \
        origin = 'native', \
        center = center, \
        width = width )

slc.set_axes_unit( LengthUnitX )

if ( ShowMesh ) : slc.annotate_cell_edges \
                    ( line_width = 1.0e-12, alpha = MeshAlpha, color = 'black' )

slc.set_cmap( blField, cmap )

slc.set_colorbar_label( Field, zLabel )

if ( not UseCustomZmin ) : zmin = 'min'
if ( not UseCustomZmax ) : zmax = 'max'

slc.set_zlim( Field, zmin = zmin, zmax = zmax )

if ( OverplotContours ) :
    slc.annotate_contour \
      ( blField, levels = nLevels, clim = (zmin,zmax) )

slc.set_log( Field, log = UseLogScaleZ )

slc.set_minorticks         ( Field, ShowMinorTicksXY )
slc.set_colorbar_minorticks( Field, ShowMinorTicksZ  )

slc.set_xlabel( xLabel )
slc.set_ylabel( yLabel )

slc.annotate_text( (0.2, 0.92),
                   PlotTitle,
                   coord_system = "figure",
                   text_args = {"color" : "black"}, )
slc.zoom( Zoom )

slc.save()

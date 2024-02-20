#!/usr/bin/env python3

from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
plt.style.use( 'publication.sty' )

import GlobalVariables.Settings as gvS
gvS.PlotDirectory = '../thornadoHydroXCFC_MethodsPaper_Data/'

from gaussxw import gaussxw

nQ = 10

def Lagrange( x, xq, i ):
    L = 1.0
    for j in range( xq.shape[0] ):
        if i != j:
            L *= ( x - xq[j] ) / ( xq[i] - xq[j] )
    return L

def rho_h( x, xq, rhoq ):
    rho = 0.0
    for i in range( xq.shape[0] ):
        rho += rhoq[i] * Lagrange( x, xq, i )
    return rho

def rhoExact( x ):
    return 1.0 + 0.1 * np.sin( 2.0 * np.pi * x )

def ComputeL1( pathToData, fileNameRoot, nN, nXC, grid, fc ):

    N = np.int64( nN )

    fileRoot \
      = '{:}{:}_nN{:}_nXC{:}_{:}{:}.plt' \
            .format( pathToData, fileNameRoot, nN, nXC, grid, fc )

    fileI = fileRoot + '_init.dat'

    dataI = np.loadtxt( fileI )
    i = 0
    levels = np.array( dataI[:,i]    , dtype = np.int64   ); i += 1
    iX1    = np.array( dataI[:,i]    , dtype = np.int64   ); i += 1
    iX2    = np.array( dataI[:,i]    , dtype = np.int64   ); i += 1
    iX3    = np.array( dataI[:,i]    , dtype = np.int64   ); i += 1
    dX1    = np.array( dataI[:,i]    , dtype = np.float64 ); i += 1
    dX2    = np.array( dataI[:,i]    , dtype = np.float64 ); i += 1
    dX3    = np.array( dataI[:,i]    , dtype = np.float64 ); i += 1
    X1n    = np.array( dataI[:,i:i+N], dtype = np.float64 ); i += N
    X2n    = np.array( dataI[:,i:i+1], dtype = np.float64 ); i += 1
    X3n    = np.array( dataI[:,i:i+1], dtype = np.float64 ); i += 1
    dataI  = np.array( dataI[:,i:i+N], dtype = np.float64 )

    nX1 = iX1.shape[0]
    nDOFX = nX1 * N

    fileF = fileRoot + '_finl.dat'

    dataF = np.loadtxt( fileF )
    i = 0
    levels = np.array( dataF[:,i]    , dtype = np.int64   ); i += 1
    iX1    = np.array( dataF[:,i]    , dtype = np.int64   ); i += 1
    iX2    = np.array( dataF[:,i]    , dtype = np.int64   ); i += 1
    iX3    = np.array( dataF[:,i]    , dtype = np.int64   ); i += 1
    dX1    = np.array( dataF[:,i]    , dtype = np.float64 ); i += 1
    dX2    = np.array( dataF[:,i]    , dtype = np.float64 ); i += 1
    dX3    = np.array( dataF[:,i]    , dtype = np.float64 ); i += 1
    X1n    = np.array( dataF[:,i:i+N], dtype = np.float64 ); i += N
    X2n    = np.array( dataF[:,i:i+1], dtype = np.float64 ); i += 1
    X3n    = np.array( dataF[:,i:i+1], dtype = np.float64 ); i += 1
    dataF  = np.array( dataF[:,i:i+N], dtype = np.float64 )

    xqN, wqN = gaussxw( N  )
    xqQ, wqQ = gaussxw( nQ )

    xL = 0.0
    Lnum = 0.0
    Lden = 0.0
    for iX1 in range( nX1 ):

        xH = xL + dX1[iX1]
        xC = 0.5 * ( xL + xH )
        x = xC + xqQ * dX1[iX1]
        xL = xH

        uqN_F = dataF[iX1]
        for q in range( nQ ):
            Lnum += dX1[iX1] * wqQ[q] * np.abs( rho_h( x[q], xqN, uqN_F ) - rhoExact( x[q] ) )
            Lden += dX1[iX1] * wqQ[q] * np.abs( rhoExact( x[q] ) )

    L1 = Lnum / Lden

    return N, nX1, L1

fig, ax = plt.subplots( 1, 1 )

nn = [ '02', '03' ]

pathToData = gvS.PlotDirectory + 'SineWaveAdvection/'
fileNameRoot = 'Advection1D_SineWaveX1'

filename = '/home/kkadoogan/Work/thornadoHydroXCFC_MethodsPaper/FluxCorrections_L1.tab'
with open( filename, 'w' ) as f:
    f.write( '% Generated by {:}\n% on {:}\n' \
             .format( __file__, datetime.today() ) )
    f.write( '\\begin{deluxetable}{ccccc}[htb!]\n' )
    f.write( '  \\tablecaption{Effect of Flux Corrections}\n' )
    f.write( '  \\tablehead{                %\n' )
    f.write( '  \colhead{$N$}              &\n' )
    f.write( '  \colhead{$\\NK$}            &\n' )
    f.write( '  \colhead{Mesh}             &\n' )
    f.write( '  \colhead{Flux Corrections} &\n' )
    f.write( '  \colhead{$E_{1}\\left[\\rho_{h}\\right]$} }\n' )
    f.write( '  \startdata\n' )

for i in range( len( nn ) ):

    narr  = []
    nxarr = []
    L1arr = []
    garr  = []
    fcarr = []

    nN = nn[i]

    nXC = '0032'

    N, nX1, L1 \
      = ComputeL1( pathToData, fileNameRoot, nN, nXC, 'Single', '' )
    narr .append( N   )
    nxarr.append( nX1 )
    L1arr.append( L1  )
    garr .append( 'Single' )
    fcarr.append( 'N/A' )

    N, nX1, L1 \
      = ComputeL1( pathToData, fileNameRoot, nN, nXC, 'Multi', '_FCT' )
    narr .append( N   )
    nxarr.append( nX1 )
    L1arr.append( L1  )
    garr .append( 'Multi' )
    fcarr.append( 'Yes' )

    N, nX1, L1 \
      = ComputeL1( pathToData, fileNameRoot, nN, nXC, 'Multi', '_FCF' )
    narr .append( N   )
    nxarr.append( nX1 )
    L1arr.append( L1  )
    garr .append( 'Multi' )
    fcarr.append( 'No' )

    nXC = '0064'

    N, nX1, L1 \
      = ComputeL1( pathToData, fileNameRoot, nN, nXC, 'Single', '' )
    narr .append( N   )
    nxarr.append( nX1 )
    L1arr.append( L1  )
    garr .append( 'Single' )
    fcarr.append( 'N/A' )

    with open( filename, 'a' ) as f:
        for i in range( len( L1arr ) ):
            exponent = np.floor( np.log10( np.abs( L1arr[i] ) ) )
            f.write( '{:} & {:} & {:} & {:} & ${:.2f}\\times10^{{{:}}}$ \\\\\n' \
                     .format( narr[i], nxarr[i], garr[i], fcarr[i], \
                              L1arr[i] / 10**( exponent ), np.int64( exponent ) ) )

    plt.loglog( np.array(narr)*np.array(nxarr), L1arr, '.', label = f'nN = {nN}' )

plt.legend()
plt.show()

with open( filename, 'a' ) as f:
    f.write( '  \enddata\n' )
    f.write( '  \label{tab.CR}\n' )
    f.write( '  \\tablecomments{Effects of flux corrections on the accuracy\n' )
    f.write( 'of our numerical method.\n' )
    f.write( 'The first column is the number of DG nodes per element,\n' )
    f.write( 'the second column is the number of elements,\n' )
    f.write( 'the third column specifies whether or not the simulation used a single-\n' )
    f.write( 'or multi-level mesh,\n' )
    f.write( 'the fourth column specifies whether or not a multi-level mesh simulation\n' )
    f.write( 'applied flux corrections,\n' )
    f.write( 'and the fifth column denotes the error as defined in\n' )
    f.write( '\myeqref{eq.Error}.}\n' )
    f.write( '\end{deluxetable}\n' )

import os
os.system( 'rm -rf __pycache__ ' )

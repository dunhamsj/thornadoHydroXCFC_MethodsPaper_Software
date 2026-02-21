#!/usr/bin/env python3

from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
plt.style.use( 'publication.sty' )

from getNodalData import getData, getQuadratureWeights1D
from myUtilitiesModule import getPlotfileNumberArray, Lagrange, rho_h

from gaussxw import gaussxw

import globalVariables as gv

rootPathToData = gv.dataDirectory + 'SineWaveAdvection/'

def get_data(nN, fileName):

    nN = np.array([nN, 1, 1], dtype = np.int64)

    data = np.loadtxt(fileName+'CF_D_proc000.dat')

    j = 0
    iLevel = np.int64  ( data[:,j]         ); j += 1
    iX1    = np.int64  ( data[:,j]         ); j += 1
    iX2    = np.int64  ( data[:,j]         ); j += 1
    iX3    = np.int64  ( data[:,j]         ); j += 1
    dx1    = np.float64( data[:,j]         ); j += 1
    dx2    = np.float64( data[:,j]         ); j += 1
    dx3    = np.float64( data[:,j]         ); j += 1
    x1n    = np.float64( data[:,j:j+nN[0]] ); j += nN[0]
    x2n    = np.float64( data[:,j:j+nN[1]] ); j += nN[1]
    x3n    = np.float64( data[:,j:j+nN[2]] ); j += nN[2]
    un     = data[:,j:]

    return iLevel.shape[0], dx1, x1n, un

def exact(x):
    W = 1.0 / np.sqrt(1.0 - 0.1**2)
    return W * (1.0 + 0.1 * np.sin( 2.0 * np.pi * x ))

data = [[2, 32 , 'Single', ''    , 'DG(1), nXC = 32'], \
        [2, 32 , 'Multi' , '_FCF', 'DG(1), nXC = 32 (F)'], \
        [2, 32 , 'Multi' , '_FCT', 'DG(1), nXC = 32 (T)'], \
        [2, 128, 'Single', ''    , 'DG(1), nXC = 128'], \
        [3, 32 , 'Single', ''    , 'DG(2), nXC = 32'], \
        [3, 32 , 'Multi' , '_FCF', 'DG(2), nXC = 32 (F)'], \
        [3, 32 , 'Multi' , '_FCT', 'DG(2), nXC = 32 (T)'], \
        [3, 128, 'Single', ''    , 'DG(2), nXC = 128']]


def computeMass(un, dx, wq):
    mass = 0.0
    for iX1 in range(dx.shape[0]):
        mass += dx[iX1] * np.sum(wq * np.abs(un[iX1]))
    return mass

nQ = 10
xqq, wq = gaussxw(nQ)
mass0 = 0.0
xl = 0.0
dx = 1.0 / 1024
for i in range(1024):
    xC = xl + 0.5 * dx
    xq = xC + dx * xqq
    mass0 += dx * np.sum(wq * np.abs(exact(xq)))
    xl += dx

def plot(nN, nXC, grid, fc, lab):

    id = 'Advection1D_SineWaveX1_nN{:}_nXC{:}_{:}{:}' \
         .format(str(nN).zfill(2), str(nXC).zfill(4), grid, fc)
    dataDirectory = rootPathToData + id + '/'

    plotfileNumberArray = getPlotfileNumberArray( dataDirectory, id, swa = True )

    nSS = plotfileNumberArray.shape[0]

    wq = getQuadratureWeights1D(nN)

    dm = np.empty(nSS, np.float64)

    for iSS in range(nSS):
        filename = dataDirectory + '{:}.plt{:}_nodal/' \
                            .format(id, str(plotfileNumberArray[iSS]).zfill(8))
        nX, dx, xn, un = get_data(nN, filename)

        dm[iSS] = computeMass(un, dx, wq)

    t = np.linspace(0, 10, dm.shape[0])

    plt.plot(t,np.abs(dm-mass0)/mass0,label=lab)

for i in range(len(data)):
    plot(data[i][0],data[i][1],data[i][2],data[i][3],data[i][4])

plt.title('Sine wave advection, ' + r'$M(t) := \int_{0}^{1} D\left(x,t\right) \, dx = \Delta x \sum_{q} w_{q} D_{q}(t)$')
plt.xlabel('time')
plt.ylabel(r'$\left|M(t)-M(0)\right|/M(0)$')
plt.yscale('log')
#plt.ylim(-1.0e-14, 1.0e-14)
plt.legend()
plt.show()
#figname = '/Users/dunhamsj/fig.png'
#plt.savefig(figname, dpi = 300)
#print('  Saved {:}'.format(figname))
import os
os.system('rm -rf __pycache__')

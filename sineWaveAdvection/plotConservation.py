#!/usr/bin/env python3

from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
plt.style.use( 'publication.sty' )

from getNodalData import getData, getQuadratureWeights1D
from myUtilitiesModule import getPlotfileNumberArray, Lagrange, rho_h

import globalVariables as gv

rootPathToData = gv.dataDirectory + 'sineWaveAdvection/'
rootPathToData = '/mnt/shared/work/codes/thornado/SandBox/AMReX/dgExperiments_Euler_Relativistic_IDEAL/'

def exact(x):
    W = 1.0 / np.sqrt(1.0 - 0.1**2)
    return W * (1.0 + 0.1 * np.sin( 2.0 * np.pi * x ))

data = [['02', '0128', 'Single', '', '2single'], \
        ['02', '0032', 'Multi', '_FCF','2multi-fcf'], \
        ['02', '0032', 'Multi', '_FCT','2multi-fct'], \
        ['03', '0128', 'Single', '', '3single'], \
        ['03', '0032', 'Multi', '_FCF','3multi-fcf'], \
        ['03', '0032', 'Multi', '_FCT','3multi-fct']]
data = [['01', '0032', 'Single', '', 'DG(0), nX=032'], \
        ['01', '0256', 'Single', '', 'DG(0), nX=256'], \
        ['02', '0032', 'Single', '', 'DG(1), nX=032'], \
        ['02', '0256', 'Single', '', 'DG(1), nX=256'], \
        ['03', '0032', 'Single', '', 'DG(2), nX=032'], \
        ['03', '0256', 'Single', '', 'DG(2), nX=256']]

gv.dataDirectory + 'sineWaveAdvection/'

def computeMass(un, dx, wq):
    mass = 0.0
    iLo = 0
    for iX1 in range(dx.shape[0]):
        iHi = iLo + wq.shape[0]
        mass += dx[iX1] * np.sum(wq * np.abs(un[iLo:iHi]))
        iLo = iHi
    return mass

def plot(nN, nXC, grid, fc, lab):

    id = 'Advection1D_SineWaveX1_nN{:}_nXC{:}_{:}{:}' \
         .format(nN, nXC, grid, fc)
    dataDirectory = rootPathToData + id + '/'

    print(dataDirectory)

    plotfileNumberArray = getPlotfileNumberArray( dataDirectory, id, swa = True )

    nSS = plotfileNumberArray.shape[0]

    wq = getQuadratureWeights1D(int(nN))

    dm = np.empty(nSS, np.float64)

    d = dataDirectory + '{:}.plt{:}_nodal/' \
                        .format(id, str(plotfileNumberArray[0]).zfill(8))
    xn, un0, dx = getData(d, 'CF_D', [int(nN), 1, 1])
    mass0 = computeMass(exact(xn), dx, wq)
    for iSS in range(nSS):
        d = dataDirectory + '{:}.plt{:}_nodal/' \
                            .format(id, str(plotfileNumberArray[iSS]).zfill(8))
        xn, un, dx = getData(d, 'CF_D', [int(nN), 1, 1])

        dm[iSS] = computeMass(un, dx, wq)

    d = dataDirectory + '{:}.plt{:}_nodal/' \
                        .format(id, str(plotfileNumberArray[-1]).zfill(8))
    xn, un, dx = getData(d, 'CF_D', [int(nN), 1, 1])
    t = np.linspace(0,10,dm.shape[0])
    plt.plot(t,(dm-mass0)/mass0,label=lab)

for i in range(len(data)):
    plot(data[i][0],data[i][1],data[i][2],data[i][3],data[i][4])

plt.title('Sine wave advection, ' + r'$M(t) := \int_{0}^{1} D\left(x,t\right) \, dx = \Delta x \sum_{q} w_{q} D_{q}(t)$')
plt.xlabel('time')
plt.ylabel(r'$\left|M(t)-M(0)\right|/M(0)$')
plt.yscale('log')
#plt.ylim(-1.0e-14, 1.0e-14)
plt.legend()
#plt.show()
figname = '/home/dunhamsj/fig.png'
plt.savefig(figname, dpi = 300)
print('  Saved {:}'.format(figname))
import os
os.system('rm -rf __pycache__')

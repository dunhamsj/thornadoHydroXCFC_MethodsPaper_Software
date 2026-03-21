#!/usr/bin/env python

from datetime import datetime
import numpy as np
from scipy.optimize import curve_fit

import matplotlib.pyplot as plt

import globalVariables as gv

from computeL1Error import computeL1error

NN   = [1, 2, 3]
Grid = ['Single', 'Multi']
FC   = ['', '_FCF', '_FCT']
NXC  = [16, 32, 64, 128, 256, 512]

pathToData = gv.dataDirectory + 'sineWaveAdvection/convergence_rates/'
fileNameRoot = pathToData + 'Advection1D_SineWaveX1'

def linear(x, m, b):
    return m * x + b

data = np.empty((len(NN), 3, 2, len(NXC)))
lab = [['DG(0), Single', \
        'DG(0), Multi, Off', \
        'DG(0), Multi, On'], \
       ['DG(1), Single', \
        'DG(1), Multi, Off', \
        'DG(1), Multi, On'], \
       ['DG(2), Single', \
        'DG(2), Multi, Off', \
        'DG(2), Multi, On']]
ls = ['-x', \
      '-s', \
      '-^']

for i in range(len(NN)):
        
    nN = NN[i]

    m = -1
    for j in range(len(Grid)):
    
        grid = Grid[j]
    
        for k in range(len(FC)):
    
            fc = FC[k]

            if ((grid == 'Single') & (fc != '')): continue
            if ((grid == 'Multi' ) & (fc == '')): continue

            m += 1
            nDOF = []
            E1   = []

            for l in range(len(NXC)):
    
                nXC = NXC[l]
    
                N, nX, L1 = computeL1error(nN, nXC, grid, fc, fileNameRoot)

                data[i,m,0,l] = N*nX
                data[i,m,1,l] = L1

                nDOF.append(np.log10(N * nX))
                E1.append(np.log10(L1))

            popt, pcov = curve_fit(linear, nDOF, E1)

            chi = popt[0]

fig, axs = plt.subplots(3, 1, figsize=(8,6))

m = -1
for i in range(len(Grid)):
    grid = Grid[i]
    for j in range(len(FC)):
        fc = FC[j]
        if ((grid == 'Single') & (fc != '')): continue
        if ((grid == 'Multi' ) & (fc == '')): continue

        m += 1

        for k in range(len(NN)):
            axs[k].loglog(data[k,m,0], data[k,m,1], \
                          ls[m], c = 'k', label = lab[k][m], fillstyle = 'none')

nDOF = np.array([20, 1000], np.float64)
dg0  = nDOF**(-1)
dg1  = 0.01*nDOF**(-2)
dg2  = nDOF**(-3)
axs[0].plot(nDOF, dg0, 'k')
axs[1].plot(nDOF, dg1, 'k')
axs[2].plot(nDOF, dg2, 'k')
axs[0].text(0.3, 0.4, r'$\propto \mathrm{nDOF}^{-1}$', c = 'k', fontsize = 10, transform = axs[0].transAxes)
axs[1].text(0.3, 0.2, r'$\propto \mathrm{nDOF}^{-2}$', c = 'k', fontsize = 10, transform = axs[1].transAxes)
axs[2].text(0.3, 0.3, r'$\propto \mathrm{nDOF}^{-3}$', c = 'k', fontsize = 10, transform = axs[2].transAxes)

plt.subplots_adjust(hspace = 0.5)
axs[0].legend(loc = 3, prop={'size':8})
axs[1].legend(loc = 3, prop={'size':8})
axs[2].legend(loc = 3, prop={'size':8})

axs[0].set_xlabel('nDOF'  , size = 12)
axs[0].set_ylabel(r'$E_1$', size = 12)
axs[1].set_xlabel('nDOF'  , size = 12)
axs[1].set_ylabel(r'$E_1$', size = 12)
axs[2].set_xlabel('nDOF'  , size = 12)
axs[2].set_ylabel(r'$E_1$', size = 12)

#plt.show()
figname = gv.paperDirectory + 'Figures/fig.convergence_rates.pdf'
plt.savefig(figname, dpi = 300)
print('  Saved {:}'.format(figname))
#plt.close()

import os
os.system( 'rm -rf __pycache__ ' )

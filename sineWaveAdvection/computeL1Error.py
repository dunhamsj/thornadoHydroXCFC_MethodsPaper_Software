#!/usr/bin/env python3

from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
plt.style.use( 'publication.sty' )

import globalVariables as gv

from gaussxw import gaussxw

pathToData = gv.dataDirectory + 'SineWaveAdvection/'
fileNameRoot = pathToData + 'Advection1D_SineWaveX1'

def Lagrange(x, xq, i):
    L = 1.0
    for j in range(xq.shape[0]):
        if i != j:
            L *= (x - xq[j]) / (xq[i] - xq[j])
    return L

def uh(x, xq, uq):
    u = 0.0
    for i in range(xq.shape[0]):
        u += uq[i] * Lagrange(x, xq, i)
    return u

def D_exact(x):
    W = 1.0 / np.sqrt(1.0 - 0.1**2) 
    return W * (1.0 + 0.1 * np.sin(2.0 * np.pi * x))

def get_data(nN, nXC, grid, FC, suffix):

    fileName = fileNameRoot \
                 + '_nN{0:}_nXC{1:}_{2:}{3:}/' \
                   .format(str(nN).zfill(2), str(nXC).zfill(4), grid, FC, suffix) \
                 + 'Advection1D_SineWaveX1_nN{0:}_nXC{1:}_{2:}{3:}.{4:}/CF_D_proc000.dat' \
                   .format(str(nN).zfill(2), str(nXC).zfill(4), grid, FC, suffix)


    nN = np.array([nN, 1, 1], dtype = np.int64)

    data = np.loadtxt(fileName)

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

nQ = 10
xqq, wq = gaussxw(nQ)
mass0 = 0.0
xl = 0.0
dx = 1.0 / 1024
for i in range(1024):
    xC = xl + 0.5 * dx
    xq = xC + dx * xqq
    mass0 += dx * np.sum(wq * np.abs(D_exact(xq)))
    xl += dx

def computeL1error(nN, nXC, grid, FC):

    nX, dx, xn, un = get_data(nN, nXC, grid, FC, 'final')

    nQ = nN
    xqq, wq = gaussxw(nQ)

    L1 = 0.0
    for i in range(nX):
        xC = np.sum(xn[i]) / xn[1].shape[0]
        xq = xC + dx[i] * xqq
        L1 += dx[i] * np.sum(wq * np.abs(uh(xq, xn[i], un[i]) - D_exact(xq)))

    return nN, nX, L1 / mass0

data = [[2, 32 , 'Single', ''    ], \
        [2, 32 , 'Multi' , '_FCF'], \
        [2, 32 , 'Multi' , '_FCT'], \
        [2, 128, 'Single', ''   ], \
        [3, 32 , 'Single', ''    ], \
        [3, 32 , 'Multi' , '_FCF'], \
        [3, 32 , 'Multi' , '_FCT'], \
        [3, 128, 'Single', ''   ]]

for i in range(len(data)):
    L1 = computeL1error(data[i][0], data[i][1], data[i][2], data[i][3])
    print(data[i], L1[-1])
import os
os.system( 'rm -rf __pycache__ ' )

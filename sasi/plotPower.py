#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt

# colorblind-friendly palette: https://gist.github.com/thriveth/8560036
color = ['#377eb8', '#ff7f00', '#4daf4a', \
         '#f781bf', '#a65628', '#984ea3', \
         '#999999', '#e41a1c', '#dede00']

dataS = np.loadtxt( 'Power_singleLevel.dat' )
dataM = np.loadtxt( 'Power_multiLevel.dat' )
#for i in range( 5 ):
for i in range( 1, 2 ):
    plt.semilogy( dataM[:,0], dataM[:,i+1], ls = '-' , c = color[i], label = 'l={:}'.format(i) )
    plt.semilogy( dataS[:,0], dataS[:,i+1], ls = '--', c = color[i], label = 'l={:}'.format(i) )

plt.legend()
plt.xlabel( 'time [ms]' )
plt.ylabel( 'Power [cgs]' )
#plt.xlim( 0, 30 )
plt.grid()
plt.title( 'Perturbation Amplitude = 0.1' )
plt.show()
#plt.savefig( 'fig.power_PA0.1_ell1.png', dpi = 300 )

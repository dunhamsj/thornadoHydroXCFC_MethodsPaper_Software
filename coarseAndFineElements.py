#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
plt.style.use( 'publication.sty' )
import matplotlib.patches as patches

import globalVariables as gv

class Draw:

    def __init__(self, N, fig, ax):

        self.N   = N
        self.fig = fig
        self.ax  = ax

        dx = 0.5
        dy = 0.5
        xC_L = 0.25
        yC_L = 0.25
        xF_L = 0.25 + 1.4 * dx
        yF_L = 0.25

        XC_C = xC_L + 0.5 * dx
        XC_F = xF_L + 0.5 * dx
        YH   = yF_L + 1.1*dy
        YL   = 0.9 * yF_L

        # Floor
        ax.plot([xC_L, xC_L + dx], [yC_L, yC_L], 'k')
        # Ceiling
        ax.plot([xC_L, xC_L + dx], [yC_L + dy, yC_L + dy], 'k')
        # Left wall
        ax.plot([xC_L, xC_L], [yC_L, yC_L + dy], 'k')
        # Right wall
        ax.plot([xC_L + dx, xC_L + dx], [yC_L, yC_L + dy], 'k')

        # Floor
        ax.plot([xF_L, xF_L + dx], [yF_L, yF_L], 'k')
        # Ceiling
        ax.plot([xF_L, xF_L + dx], [yF_L + dy, yF_L + dy], 'k')
        # Left wall
        ax.plot([xF_L, xF_L], [yF_L, yF_L + dy], 'k')
        # Right wall
        ax.plot([xF_L + dx, xF_L + dx], [yF_L, yF_L + dy], 'k')

        self.GetQuadrature()

        # Points in coarse element

        xC = xC_L + 0.5 * dx
        yC = yC_L + 0.5 * dy
        xx = xC + self.xq * dx
        yy = yC + self.xq * dy
        for i in range(N):
            for j in range(N):
                ax.plot(xx[i], yy[j], 'k.')

        for i in range(N):
            ax.plot(xC_L     , yy[i]    , 'ks')
            ax.plot(xC_L + dx, yy[i]    , 'ks')
            ax.plot(xx[i]    , yC_L     , 'ks')
            ax.plot(xx[i]    , yC_L + dy, 'ks')

        ax.plot([xF_L, xF_L + dx], [yF_L + 0.5 * dy, yF_L + 0.5 * dy], 'k')
        ax.plot([xF_L + 0.5 * dx, xF_L + 0.5 * dx], [yF_L, yF_L + dy], 'k')

        ax.text(xC - 0.07 * dx, yC, r'$U_{h}$')

        # Points in fine element (1,1)

        dx *= 0.5
        dy *= 0.5

        xL = [ xF_L     , xF_L + dx    , xF_L         , xF_L + dx]
        xH = [ xF_L + dx, xF_L + 2 * dx, xF_L + dx    , xF_L + 2 * dx]
        yL = [ yF_L     , yF_L         , yF_L + dy    , yF_L + dy]
        yH = [ yF_L + dy, yF_L + dy    , yF_L + 2 * dy, yF_L + 2 * dy]

        text = [r'$u_{h}^{(1)}$', \
                r'$u_{h}^{(2)}$', \
                r'$u_{h}^{(3)}$', \
                r'$u_{h}^{(4)}$']
        for k in range(len(xL)):

            xC = xL[k] + 0.5 * dx
            yC = yL[k] + 0.5 * dy
            xx = xC + self.xq * dx
            yy = yC + self.xq * dy
            for i in range(N):
                for j in range(N):
                    ax.plot(xx[i], yy[j], 'k.')
    
            for i in range(N):
                ax.plot(xL[k]     , yy[i]    , 'ks')
                ax.plot(xL[k] + dx, yy[i]    , 'ks')
                ax.plot(xx[i]    , yL[k]     , 'ks')
                ax.plot(xx[i]    , yL[k] + dy, 'ks')

            ax.text(xC-0.15*dx, yC, text[k])

        style = "Simple, tail_width=0.5, head_width=4, head_length=8"
        kw = dict(arrowstyle=style, color = 'k')

        a1 = patches.FancyArrowPatch((XC_C, YH), (XC_F, YH), \
                                     connectionstyle="arc3, rad=-0.5", **kw)
        plt.gca().add_patch(a1)
        ax.text( 0.4 * (XC_C + XC_F), YH * (1+0.3), 'Coarse-to-Fine')

        a2 = patches.FancyArrowPatch((XC_F, YL), (XC_C, YL), \
                                     connectionstyle="arc3, rad=-0.5", **kw)
        plt.gca().add_patch(a2)
        ax.text( 0.4 * (XC_C + XC_F), YL * (1-1.1), 'Fine-to-Coarse')

        return


    def GetQuadrature(self):

        if self.N == 1:

            wq = np.array([ +1.0 ], np.float64)
            xq = np.array([ +0.0 ], np.float64)

        elif self.N == 2:

            wq = np.array([ +1.0, +1.0 ], np.float64) / 2.0
            xq = np.array([ -1.0, +1.0 ], np.float64) / np.sqrt( 12.0 )

        elif self.N == 3:

            wq = np.array([ +5.0, +8.0, +5.0 ], np.float64) / 18.0
            xq = np.array([ -1.0, +0.0, +1.0 ], np.float64) \
                   * np.sqrt( 3.0 / 20.0 )

        else:

          print( 'Invalid choice of N: {:}'.format( self.N ) )
          exit( 'Exiting...' )

        self.wq = wq
        self.xq = xq

        return


if __name__ == '__main__':

    N = 2
    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    ax.xaxis.set_visible( False )
    ax.yaxis.set_visible( False )
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['right'].set_visible(False)

    D = Draw(N, fig, ax)

    figName = gv.paperDirectory + 'Figures/fig.coarseAndFine.pdf'
    plt.savefig(figName, dpi = 300, bbox_inches = 'tight')
    print('\n  Saved {:}'.format(figName))
    #plt.show()
    plt.close()

    import os
    os.system( 'rm -rf __pycache__' )

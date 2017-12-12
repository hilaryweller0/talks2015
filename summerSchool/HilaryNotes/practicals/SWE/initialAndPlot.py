# Code for initialising and plotting results of the A and C-grid codes 

import numpy as np
import matplotlib.pyplot as plt

def initialJetu(nx, y, SWEparams):
    "Calculate the initial velocity field for the geostrophically balanced"
    "jet at nx x locations and y locations"
    
    # jet parameters
    yc = SWEparams['yc']
    jetw = SWEparams['jetw']
    umax = SWEparams['umax']

    # derived jet parameters
    yhat = (y - yc)/jetw
    
    # initialise u
    u = np.zeros([nx, np.size(y)])
    u[:,:] = np.where((abs(yhat) > 1), 0., \
                      umax*(1 - 3*yhat**2 + 3*yhat**4 - yhat**6))

    return u

def initialJeth(nx, y, SWEparams):
    "Calculate the initial height field for the geostrophically balanced"
    "jet at nx x locations and y locations"

    # jet parameters
    yc = SWEparams['yc']
    jetw = SWEparams['jetw']
    beta = SWEparams['beta']
    umax = SWEparams['umax']
    g = SWEparams['g']

    # derived jet parameters
    yhat = (y - yc)/jetw
    hS = 16./35*jetw*beta*umax*yc/g      # southern h
    hN = -hS                             # northern h
    
    # initialise h
    h = np.zeros([nx, np.size(y)])
    h[:,:] = np.where((yhat < -1), hS, np.where((yhat > 1), hN,
                   hS - jetw*beta*umax/g*(
                   yc*(16./35+yhat-yhat**3+3./5*yhat**5-1./7*yhat**7)
                 + jetw
            *(-1./8+0.5*yhat**2-0.75*yhat**4+0.5*yhat**6-1./8*yhat**8))))

    return h


def createMountain(grid, SWEparams):
    "create the mountain, h0 on the grid using parameters in SWEparams"
    
    # mountain parameters
    xc = SWEparams['xc']
    yc = SWEparams['yc']
    rm = SWEparams['rm']
    h0max = SWEparams['h0max']
    
    h0 = np.zeros([grid.nx,grid.ny])

    return h0


def plothuv(grid, h, h0, u, v, title=''):
    "plot the height and velocity for A- or C-grid variables"
    plt.clf()
    # plot h on grid boxes
    plt.colorbar(plt.pcolormesh(grid.xp, grid.yp, np.transpose(h+h0)))
    
    if (np.max(h0) > np.min(h0)): # plot the mountain if non-zero
        plt.contour(grid.x, grid.y, np.transpose(h0))
    
    # plot velocity vectors if coarse resolution
    if grid.nx <= 50 and grid.ny <= 50:
        if (np.shape(v) == np.shape(h)): # plot velocity vectors for A-grid
            plt.quiver(grid.x, grid.y, np.transpose(u), np.transpose(v), scale=1e3)
        else: # plot velocity vectors for C-grid
            # (with interpolated tangential components)
            plt.quiver(grid.xu, grid.yu, np.transpose(u), np.transpose(vatu(v)),
                       scale=1e3)
            plt.quiver(grid.xv, grid.yv, np.transpose(uatv(u)), np.transpose(v),
                       scale=1e3)
    # Define the axes and show the plot
    plt.axis([grid.xmin, grid.xmax, grid.ymin, grid.ymax])
    plt.title(title)
    plt.draw()


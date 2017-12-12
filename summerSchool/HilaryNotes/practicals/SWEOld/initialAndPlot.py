# Code for initialising and plotting results of the A and C-grid codes 

import numpy as np
import matplotlib.pyplot as plt

def initialJet(nx, y, beta, g, yc, jetw, umax):
    "Calculate the initial conditions for the geostrophically balanced jet"
    "for h, u and v at nx x-locations and at locations y"
    
    # derived jet parameters
    yS = yc - jetw    # Southern extent of the jet
    yN = yc - jetw    # Northern extent of the jet
    yhat = (y - yc)/jetw
    hS = 16./35*jetw*beta*umax*yc/g  # southern h
    hN = -hS                     # northern h
    
    ny = len(y)
    
    # initialise u, v and h
    u = np.zeros([nx, ny])
    v = np.zeros([nx, ny])
    h = np.zeros([nx, ny])

    # jet velocity
    u[:,:] = np.where((abs(yhat) > 1), 0., \
             umax*(1 - 3*yhat**2 + 3*yhat**4 - yhat**6))

    # jet height
    h[:,:] = np.where((yhat < -1), hS, np.where((yhat > 1), hN, \
                hS - jetw*beta*umax/g*(\
             yc*(16./35+yhat-yhat**3+3./5*yhat**5-1./7*yhat**7)\
           + jetw*(-1./8+0.5*yhat**2-0.75*yhat**4+0.5*yhat**6-1./8*yhat**8))))

    return [h,u,v]


def createMountain(x, y, xc, yc, rm, h0max):
    "create the mountain at locations x and y"
    nx = len(x)
    ny = len(y)
    h0 = np.zeros([nx,ny])
    
    return h0


def plothuv(xh, yh, xu, yu, xv, yv, h, h0, u, v, title=''):
    "plot the height and velocity for A- or C-grid variables"
    dx = xh[-1]-xh[-2]
    dy = yh[-1]-yh[-2]
    plt.clf()
    # define x and y variables for plotting h
    x = np.append(xh-0.5*dx, xh[-1]+0.5*dx)
    y = np.append(yh-0.5*dy, yh[-1]+0.5*dy)
    # plot h on grid boxes
    plt.colorbar(plt.pcolormesh(x, y, np.transpose(h+h0)))
    if (np.max(h0) > np.min(h0)): # plot the mountain if non-zero
        plt.contour(xh, yh, np.transpose(h0))
    # plot velocity vectors if coarse resolution
    if len(xu) <= 40 & len(yu) <= 40:
        if (xh == xu).all(): # plot velocity vectors for A-grid
            plt.quiver(xu, yu, np.transpose(u), np.transpose(v), scale=1e3)
        else: # plot velocity vectors for C-grid
            # (with interpolated tangential components)
            plt.quiver(xu, yu, np.transpose(u), np.transpose(vatu(v)), scale=1e3)
            plt.quiver(xv, yv, np.transpose(uatv(u)), np.transpose(v), scale=1e3)
    # Define the axes and show the plot
    plt.axis([np.min(x), np.max(x), np.min(y), np.max(y)])
    plt.title(title)
    plt.draw()


# Code for initialising, solving and plotting the SWE on a beta-plane using
#  forward-backward time-stepping on the A- and C-grid domain periodic in x,
# slip at y boundaries

import numpy as np
import matplotlib.pyplot as plt

execfile("ACgrids.py")
execfile("initialAndPlot.py")

def main():

    # Define variables from the SWEparameters.py file
    SWEparams = {}
    execfile("SWEparameters.py", SWEparams)
    # time-stepping parameters
    nt = SWEparams['nt']            # total number of time-steps
    ntPlot = SWEparams['ntPlot']    # plot every ntPlot time-steps
    dt = SWEparams['dt']            # time-step (seconds)
    # The domain
    xmin = SWEparams['xmin']
    xmax = SWEparams['xmax']
    ymin = SWEparams['ymin']
    ymax = SWEparams['ymax']
    # number of points in the x and y directions
    nx = SWEparams['nx']
    ny = SWEparams['ny']
    # model parameters
    beta = SWEparams['beta']
    g = SWEparams['g']
    H = SWEparams['H']

    # Initial jet parameters
    yc = SWEparams['yc']            # Centre of jet
    jetw = SWEparams['jetw']        # Jet half width
    umax = SWEparams['umax']        # Maximum jet velocity
    
    # mountain parameters
    xc = SWEparams['xc']            # mountain centre
    yc = SWEparams['yc']
    rm = SWEparams['rm']            # mountain radius
    h0max = SWEparams['h0max']      # mountain peak height

    # grid-spacing
    dx = (xmax - xmin)/nx
    dy = (ymax - ymin)/ny
    # x and y locations for the h positions
    x = np.linspace(xmin + dx/2., xmax - dx/2., nx)
    y = np.linspace(ymin + dy/2., ymax - dy/2., ny)
    # x and y locations for the u positions (for the C-grid)
    xu = np.linspace(xmin, xmax - dx, nx)
    yu = np.linspace(ymin + dy/2., ymax - dy/2., ny)
    # x and y locations for the v positions (for the C-grid)
    xv = np.linspace(xmin + dx/2., xmax - dx/2., nx)
    yv = np.linspace(ymin, ymax - dy, ny)

    # Calculate the mountain height
    h0 = createMountain(x, y, xc, yc, rm, h0max)

    # Initialise u, v and h (for the C-grid)
    [hC, uC, vC] = initialJet(nx, y, beta, g, yc, jetw, umax)
    # Initialise u, v and h (for the A-grid)
    [hA, uA, vA] = initialJet(nx, y, beta, g, yc, jetw, umax)

    # Subtract the mountain height
    hC = hC - h0
    hA = hA - h0

    # Gravity wave and advective Courant number
    Cu = dt*max(np.max(uC), np.max(vC))/min(dx,dy)
    Cg = dt*np.sqrt(g*H)/min(dx,dy)
    print 'Maximum advective Courant number ', Cu, \
          '\nmaximum gravity wave Courant number ', Cg

    # plot the initial conditions
    plt.ion()
    plt.figure(1)
    plothuv(x, y, xu, yu, xv, yv, hC, h0, uC, vC, \
            title='C-grid initial conditions')
    plt.figure(2)
    plothuv(x, y, x, y, x, y, hA, h0, uA, vA, \
            title='A-grid initial conditions')

    # solve the SWE using the A- and C-grids and plot every ntPlot time steps
    for it in range(0,nt,ntPlot):
        [uC,vC,hC] = SWE_Cgrid(beta, g, H, dx, yu, yv, dt, ntPlot, uC, vC, hC,h0)
        plt.figure(1)
        plothuv(x, y, xu,yu, xv, yv, hC, h0, uC, vC, \
                title='C-grid results after time ' + str((it+ntPlot)*dt))
        
        [uA,vA,hA] = SWE_Agrid(beta, g, H, dx, y, dt, ntPlot, uA, vA, hA, h0)
        plt.figure(2)
        plothuv(x, y, x,y, x, y, hA, h0, uA, vA, \
                title='A-grid results after time ' + str((it+ntPlot)*dt))

main()


### Copy out most of this code. Code commented with 3#s (like this) ###
### is here to help you to learn python and need not be copied      ###

# Numerical schemes for simulating linear advection for outer code
# linearAdvectUni.py and linearAdvectNonU.py using uniform and 
# non-uniform grids

### The numpy package for numerical functions and pi                ###
import numpy as np

### The matplotlib package contains plotting functions              ###
import matplotlib.pyplot as plt

def plotSolution(x, phi):
    "Plot the solution during a simulation"
    font = {'size'   : 14}
    plt.rc('font', **font)
    plt.figure(2)
    plt.clf()
    plt.plot(x, phi)
    plt.ylim([-0.2,1.2])
    plt.xlabel('x')
    plt.ylabel('$\phi$')
    plt.axhline(0, linestyle=':', color='black')
    plt.axvline(0, linestyle=':', color='black')
    plt.draw()

def FTCS(x, phiOld, c, nt):
    "Linear advection of profile in phiOld using FTCS, Courant number c"
    "for nt time-steps"
    
    # the number of independent points
    nx= len(x)
    
    # new time-step array for phi
    phi = np.zeros_like(phiOld)

    # plot results as we go along
    plotSolution(x, phi)

    # FTCS for each time-step
    for it in xrange(nt):
        # Loop through all space using remainder after division (%)
        # to cope with periodic boundary conditions
        for i in xrange(nx):
            phi[i] = phiOld[i] \
                   - 0.5*c*(phiOld[(i+1)%nx] - phiOld[(i-1)%nx])
        
        # update arrays
        phiOld = phi.copy()

        # plot for this time-step
        plotSolution(x, phi)
    
    return phi

def FTCSnonU(x, phiOld, u, dt, nt):
    "Linear advection of phiOld using FTCS on a non-uniform grid as defined"
    "in array x using wind speed u, time step dt for nt time-steps"

    # grid intervals on the non-uniform grid
    dx = (np.roll(x,-1) - x)%1.
    print x
    print (np.roll(x,-1) - x)
    print dx
    print (np.max(x)-np.min(x))
    
    # Courant numbers on the non-uniform grid
    c = 2*u*dt/(dx + np.roll(dx, -1))
    
    # the number of independent points
    nx= len(x)
    
    # new time-step array for phi
    phi = np.zeros_like(phiOld)

    # plot results as we go along
    plotSolution(x, phi)

    # FTCS for each time-step
    for it in xrange(nt):
        # Loop through all space using remainder after division (%)
        # to cope with periodic boundary conditions
        for i in xrange(nx):
            phi[i] = phiOld[i] \
                   - 0.5*c[i]*(phiOld[(i+1)%nx] - phiOld[(i-1)%nx])
        
        # update arrays
        phiOld = phi.copy()

        # plot for this time-step
        plotSolution(x, phi)
    
    return phi



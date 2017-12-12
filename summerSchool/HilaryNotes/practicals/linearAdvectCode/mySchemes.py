### Copy out most of this code. Code commented with 3#s (like this) ###
### is here to help you to learn python and need not be copied      ###

# Numerical schemes for simulating linear advection for outer code
# linearAdvectUni.py and linearAdvectNonU.py using uniform and 
# non-uniform grids

### The numpy package for numerical functions and pi                ###
import numpy as np

def FTCS(grid, time, phiOld, c):
    "Linear advection of profile in phiOld using FTCS, Courant number c"
    "for number of time-steps specified in time"
    
    # new time-step array for phi
    phi = np.zeros_like(phiOld)

    # plot results as we go along
    plotSolution(grid.x, phi)

    # FTCS for each time-step
    for it in xrange(time.nt):
        # Loop through all space using remainder after division (%)
        # to cope with periodic boundary conditions
        for i in xrange(grid.nx):
            phi[i] = phiOld[i] - 0.5*c*\
                     (phiOld[(i+1)%grid.nx] - phiOld[(i-1)%grid.nx])
        
        # update arrays
        phiOld = phi.copy()

        # plot for this time-step
        plotSolution(grid.x, phi)
    
    return phi

def FTCSnonU(grid, time, phiOld, u):
    "Linear advection of phiOld using FTCS on a non-uniform grid"
    "using wind speed u"

    # Courant numbers on the non-uniform grid
    c = 2*u*time.dt/(grid.dx + np.roll(grid.dx, -1))
    
    # new time-step array for phi
    phi = np.zeros_like(phiOld)

    # plot results as we go along
    plotSolution(grid.x, phi)

    # FTCS for each time-step
    for it in xrange(time.nt):
        # Loop through all space using remainder after division (%)
        # to cope with periodic boundary conditions
        for i in xrange(grid.nx):
            phi[i] = phiOld[i] - 0.5*c[i]*\
                     (phiOld[(i+1)%grid.nx] - phiOld[(i-1)%grid.nx])
        
        # update arrays
        phiOld = phi.copy()

        # plot for this time-step
        plotSolution(grid.x, phi)
    
    return phi



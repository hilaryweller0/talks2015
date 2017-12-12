### Copy out most of this code. Code commented with 3#s (like this) ###
### is here to help you to learn python and need not be copied      ###

### Note that blocks are defined by indendtation in Python. You     ###
### should never mix tabs and spaces for indentation - use 4 spaces.###
### Setup your text editor to insert 4 spaces when you press tab    ###

# Outer code for setting up the linear advection problem on a uniform
# grid and calling the function to perform the linear advection and plot

### The numpy package for numerical functions and pi                ###
import numpy as np

### The matplotlib package contains plotting functions              ###
import matplotlib.pyplot as plt

# all the linear advection schemes and initial conditions
### Change "mySchemes.py" to the name of your file, "yourName.py".  ###
### You can also include other people's code here                   ###
execfile("mySchemes.py")
execfile("initialConditions.py")

### The main code is inside a function to avoid global variables    ###
def main():
    
    # input variables
    xmax = 1.0             # limits of the geometry
    xmin = 0.0             # (must be real numbers, not integers)
    nx = 100               # number of intervals to divide the geometry
    nt = 100               # number of time steps
    c = 0.2                # Courant number for the advection
    dx = (xmax - xmin)/nx  # spatial resolution
    u = 1.0                # wind speed
    dt = c*dx/u            # time step

    # spatial points for plotting and for defining initial conditions
    x = np.arange(xmin, xmax, dx)

    # initial conditions
    initialConditions = mixed
    ### can choose any funciton from initialConditions.py ###
    phiOld = initialConditions(x)

    # Exact solution is the same as the initial conditions but moved
    # around the periodic domain
    phiExact = initialConditions((x - u*nt*dt)%(xmax - xmin))

    # Function for advecting the profile using FTCS for nt time steps
    phiFTCS = FTCS(x, phiOld.copy(), c, nt)

    # plot options (large fonts)
    font = {'size'   : 14}
    plt.rc('font', **font)

    # plot the results versus the analytic solution
    plt.figure(1)
    plt.clf()
    plt.ion()
    plt.plot(x, phiOld,      'k--', label='Initial')
    plt.plot(x, phiExact,    'k', label='Exact')
    plt.plot(x, phiFTCS,     'r', label='FTCS')
    plt.legend(loc='best')
    plt.xlabel('x')
    plt.ylabel('$\phi$')
    plt.axhline(0, linestyle=':', color='black')
    plt.savefig('phi.pdf')

    # calculate the error norms, mean and standard deviation
    FTCSerror = phiFTCS - phiExact
    FTCS_l2error = np.std(FTCSerror)/np.std(phiExact)
    FTCS_linf = np.max(np.abs(FTCSerror))/np.max(np.abs(phiExact))
    print "FTCS l2 and linf errors", FTCS_l2error, FTCS_linf
    print "Initial mean and std deviation", np.mean(phiOld), \
           np.std(phiOld)
    print "FTCS mean and std deviation", np.mean(phiFTCS), \
          np.std(phiFTCS)

main()


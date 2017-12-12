### Copy out most of this code. Code commented with 3#s (like this) ###
### is here to help you to learn python and need not be copied      ###

### Note that blocks are defined by indendtation in Python. You     ###
### should never mix tabs and spaces for indentation - use 4 spaces.###
### Setup your text editor to insert 4 spaces when you press tab    ###

# Outer code for setting up the linear advection problem on a non-uniform
# grid and calling the function to perform the linear advection and plot

### The numpy package for numerical functions and pi                ###
import numpy as np

### The matplotlib package contains plotting functions              ###
import matplotlib.pyplot as plt

# all the linear advection schemes and initial conditions
### Change "mySchemes.py" to the name of your file, "yourName.py".  ###
### You can also include other people's code here                   ###
execfile("spaceTime.py")
execfile("initialConditions.py")
execfile("mySchemes.py")
execfile("diagnostics.py")

### The main code is inside a function to avoid global variables    ###
def main():
    
    ### Declare an instance of the GridNonU class, called grid      ###
    ### which defines the grid for these simulations. Thus grid.dx  ###
    ### and grid.nx will automatically be defined
    xmax = 1.0
    xmin = 0.0
    xmid = 0.4
    nx1 = 40
    nx2 = 40
    xtmp = np.concatenate((np.linspace(xmin, xmid, nx1, endpoint=False), \
                           np.linspace(xmid, xmax, nx2, endpoint=False)))
    grid = GridNonU(xtmp, xmax = xmax)

    # the wind speed
    u = 1.0
    
    ### Declare an instance of the Time class, called time which    ###
    ### defines the variables associated with time for these runs.  ###
    time = Time(dt = 0.2/100, nt = 100)

    # Select which initial conditions function to use
    ### can choose any funciton from initialConditions.py ###
    initialConditions = cosBell

    # Initialise dependent variable
    phiOld = initialConditions(grid.x)

    # Exact solution is the same as the initial conditions but moved
    # around the periodic domain
    phiExact = initialConditions((grid.x - u*time.endTime)%grid.length)

    # Function for advecting the profile using FTCS for nt time steps
    phiFTCS = FTCSnonU(grid, time, phiOld.copy(), u)

    ### Create and save plot                                        ###
    plotFinal(grid.x, phiFTCS, phiExact, 'FTCS', 'phiFTCSnonU.pdf')

    # calculate the error norms, mean and standard deviation
    noErrors = errorDiagnostics(grid, phiExact, phiExact)
    noErrors.write("Exact")
    FTCSerrors = errorDiagnostics(grid, phiFTCS, phiExact)
    FTCSerrors.write("FTCSnonU")

main()


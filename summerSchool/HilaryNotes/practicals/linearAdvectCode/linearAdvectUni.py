### Copy out most of this code. Code commented with 3#s (like this) ###
### is here to help you to learn python and need not be copied      ###

### Note that blocks are defined by indendtation in Python. You     ###
### should never mix tabs and spaces for indentation - use 4 spaces.###
### Setup your text editor to insert 4 spaces when you press tab    ###

# Outer code for setting up the linear advection problem on a uniform
# grid and calling the function to perform the linear advection and plot

# all the linear advection schemes and initial conditions
### Change "mySchemes.py" to the name of your file, "yourName.py".  ###
### You can also include other people's code here                   ###
execfile("spaceTime.py")
execfile("initialConditions.py")
execfile("mySchemes.py")
execfile("diagnostics.py")

### The main code is inside a function to avoid global variables    ###
def main():
    ### Declare an instance of the Grid class, called grid which    ###
    ### defines the grid for these simulations. Thus grid.dx and    ###
    ### grid.x will automatically be defined
    grid = Grid(xmin = 0.0, xmax = 1.0, nx = 100)

    ### input variables not associated with any classes             ###
    c = 0.2                # Courant number for the advection
    u = 1.0                # wind speed

    ### Declare an instance of the Time class, called time which    ###
    ### defines the variables associated with time for these runs.  ###
    time = Time(dt = c*grid.dx/u, nt = 100)

    # Select which initial conditions to use (from initialConditions.py
    initialConditions = cosBell
    # Initialise dependent variable
    phiOld = initialConditions(grid.x)
    # Exact solution is the initial condition shifted around the domain
    phiExact = initialConditions((grid.x - u*time.endTime)%grid.length)

    # Advect the profile using FTCS for all the time steps
    phiFTCS = FTCS(grid, time, phiOld.copy(), c)

    ### Create and save plot                                        ###
    plotFinal(grid.x, phiFTCS, phiExact, 'FTCS', 'phiFTCS.pdf')

    # calculate the error norms, mean and standard deviation
    noErrors = errorDiagnostics(grid, phiExact, phiExact)
    noErrors.write("Exact")
    FTCSerrors = errorDiagnostics(grid, phiFTCS, phiExact)
    FTCSerrors.write("FTCS")
    
main()


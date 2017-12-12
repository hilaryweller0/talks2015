# Parameters for the SWE solvers

# time-stepping parameters
nt = 288         # total number of time-steps
ntPlot = 12      # plot every ntPlot time-steps
dt = 300         # time-step (seconds)
# The domain
xmin = 0.
xmax = 1.2e7
ymin = 0.
ymax = 1.2e7
# number of points in the x and y directions
nx = 79
ny = 79
# model parameters
beta = 2e-11
g = 10.
H = 3000.

# Initial jet parameters
yc = 6e6          # Centre of jet
jetw = 3e6        # Jet half width
umax = 20.        # Maximum jet velocity

# mountain parameters
xc = 0.5*(xmin + xmax)         # mountain centre
yc = 0.5*(ymin + ymax)
rm = 1.5e6                     # mountain radius
h0max = 500.                   # mountain peak height

### Copy out most of this code. Code commented with 3#s (like this) ###
### is here to help you to learn python and need not be copied      ###

# Data structures for the linear advection

### The numpy package for numerical functions and pi                ###
import numpy as np

### The class, or data-structure, Grid, stores all of the grid data ###
### so that all of the grid data can be passed to functions as one. ###
### The Grid function __init__ initialises the Grid class. From     ###
### within a class definition, "self" refers to the class itself    ###
class Grid(object):
    "Store all grid data and calculates dx and x locations."
    "The grid is assumed periodic."
### There are 2 underscores before the init and 2 after             ###
    def __init__(self, xmin=0.0, xmax=1.0, nx=100):
        self.xmin = xmin
        self.xmax = xmax
        self.nx = nx
        self.length = self.xmax - self.xmin
        self.dx = self.length/self.nx
        # The x locations, excluding the end point
        self.x = np.arange(self.xmin, self.xmax, self.dx)
        self.dxs = (np.roll(self.x, -1) - self.x)%self.length


### The class Time stores all of the data associated with time and  ###
### time-stepping                                                   ###
class Time(object):
    "Data associated with time and time-stepping"
    def __init__(self, dt, nt):
        self.dt = dt
        self.nt = nt
        self.endTime = dt*nt

### The class for the non-uniform Grid. You only need to copy out   ###
### this code if you are using the non-uniform grid functions       ###
class GridNonU(object):
    "Data for non-uniform, periodic grids"
    def __init__(self, x, xmax):
        self.x = x
        self.xmax = xmax
        self.nx = len(x)
        self.xmin = self.x[0]
        self.length = self.xmax - self.xmin
        self.dx = (np.roll(x, -1) - x)%self.length
        self.dxs = self.dx


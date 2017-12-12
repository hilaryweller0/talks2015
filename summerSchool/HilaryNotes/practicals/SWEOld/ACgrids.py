# Functions for calculating gradients and divergences on the A- and C-grids
# and for interpolating variables to different locations for the C-grid

import numpy as np

def uatv(u):
    "Interpolates u to v points for the C-grid (using the average of 4"
    "surrounding u values"
    [nx,ny] = np.shape(u)
    uatv = np.zeros_like(u)
    # loop through x and y directions of u
    for i in xrange(-1,nx-1):
        for j in xrange(1,ny):
            uatv[i,j] = 0.25*(u[i,j] + u[i+1,j] + u[i,j-1] + u[i+1,j-1])
    return uatv

def vatu(v):
    "Interpolates v to u points for the C-grid (using the average of 4"
    "surrounding v values"
    [nx,ny] = np.shape(v)
    vatu = np.zeros_like(v)
    # loop through x and y directions of v
    for i in xrange(-1,nx-1):
        for j in xrange(0,ny-1):
            vatu[i,j] = 0.25*(v[i-1,j] + v[i-1,j+1] + v[i,j] + v[i,j+1])
        vatu[i,ny-1] = 0.25*(v[i-1,ny-1] + v[i,ny-1])
    return vatu

def hatu(h):
    "Transforms h to u points for the C-grid (using the average of 2"
    "adjacent h values"
    [nx,ny] = np.shape(h)
    hatu = np.zeros_like(h)
    # loop through x and y directions of h
    for i in xrange(-1,nx-1):
        for j in xrange(0,ny):
            hatu[i,j] = 0.5*(h[i-1,j] + h[i,j])
    return hatu

def hatv(h):
    "Transforms h to v points for the C-grid (using the average of 2"
    "adjacent h values"
    [nx,ny] = np.shape(h)
    hatv = np.zeros_like(h)
    # loop through x and y directions of h
    for i in xrange(-1,nx-1):
        hatv[i,0] = h[i,0]
        for j in xrange(1,ny):
            hatv[i,j] = 0.5*(h[i,j-1] + h[i,j])
    return hatv

def ddxC(f, dx):
    "Calculates the C-grid ddx of 2d array f at the staggered locations"
    [nx,ny] = np.shape(f)
    dfdx = np.zeros_like(f)

    for i in xrange(-1,nx-1):
        for j in xrange(0,ny):
            dfdx[i,j] = (f[i,j] - f[i-1,j])/dx
    return dfdx


def ddyC(f, dy):
    "Calculates the C-grid ddy of 2d array f at the staggered locations"
    [nx,ny] = np.shape(f)
    dfdy = np.zeros_like(f)

    for i in xrange(-1,nx-1):
        for j in xrange(1,ny):
            dfdy[i,j] = (f[i,j] - f[i,j-1])/dy
    return dfdy


def divC(u, v, dx, dy):
    "Calculates the divergence of u and v for the C-grid"
    [nx,ny] = np.shape(u)
    divu = np.zeros_like(u)
    
    for i in xrange(-1,nx-1):
        for j in xrange(0,ny-1):
            divu[i,j] = (u[i+1,j]-u[i,j])/dx + (v[i,j+1]-v[i,j])/dy
        divu[i,ny-1] = (u[i+1,ny-1]-u[i,ny-1])/dx - v[i,ny-1]/dy
    return divu


def ddxA(f, dx):
    "Calculates the A-grid ddx of 2d array f"
    [nx,ny] = np.shape(f)
    dfdx = np.zeros_like(f)

    for i in xrange(-1,nx-1):
        for j in xrange(1,ny-1):
            dfdx[i,j] = (f[i+1,j] - f[i-1,j])/(2.*dx)
        dfdx[i,0] = 0
        dfdx[i,ny-1] = 0
    return dfdx


def ddyA(f, dy):
    "Calculates the A-grid ddy of 2d array f"
    [nx,ny] = np.shape(f)
    dfdy = np.zeros_like(f)

    for i in xrange(-1,nx-1):
        for j in xrange(1,ny-1):
            dfdy[i,j] = (f[i,j+1] - f[i,j-1])/(2.*dy)
        dfdy[i,0] = 0  #(f[i,1] - f[i,0])/(2*dy)
        dfdy[i,ny-1] = 0  #(f[i,ny-1] - f[i,ny-2])/(2*dy)
    return dfdy


def divA(u, v, dx, dy):
    "Calculates the divergence of u and v for the A-grid"
    [nx,ny] = np.shape(u)
    divu = np.zeros_like(u)
    
    for i in xrange(-1,nx-1):
        for j in xrange(1,ny-1):
            divu[i,j] = (u[i+1,j] - u[i-1,j])/(2.*dx) \
                      + (v[i,j+1] - v[i,j-1])/(2.*dy)
        divu[i,0] = (u[i+1,0] - u[i,0])/(2.*dx) \
                  + (v[i,1] + v[i,0])/(2*dy)
        divu[i,ny-1] = (u[i+1,ny-1] - u[i-1,ny-1])/(2.*dx) \
                     - (v[i,ny-1] + v[i,ny-2])/(2*dy)
    return divu


def SWE_Cgrid(beta, g, H, dx, yu, yv, dt, nt, u, v, h, h0):
    "solves the SWE using forward-backward time-stepping and the C-grid"
    "doubly periodic domain starting from u, v and h"
    
    # Derive variables that depend on the inputs
    [nx,ny] = np.shape(u)
    dy = yu[1] - yu[0]
    H = H*np.ones_like(h)
    
    # loop through all times
    for it in xrange(nt):
        # update old values
        uOld = u.copy()
        vOld = v.copy()
        hOld = h.copy()
        
        # alternate between calculating u or v first
        for iu in xrange(2):
            if iu%2 == 0:
                # loop over x and y directions (using i and j)
                u = uOld + dt*(beta*yu*vatu(v) - g*ddxC(h,dx))
                
            else:
                v = vOld + dt*(-beta*yv*uatv(u) - g*ddyC(h,dy))

        # then calculate h using updated values of u and v
        h = hOld - dt*divC(hatu(H)*u,hatv(H)*v,dx,dy)

    return [u,v,h]


def SWE_Agrid(beta, g, H, dx, y, dt, nt, u, v, h, h0):
    "solves the SWE using forward-backward time-stepping and the A-grid"
    "doubly periodic domain stating from u, v and h"
    
    # Derive variables that depend on the inputs
    [nx,ny] = np.shape(u)
    dy = y[1] - y[0]
    
    # loop through all times
    for it in xrange(nt):
        # update old values
        uOld = u.copy()
        vOld = v.copy()
        hOld = h.copy()
        
        # alternate between calculating u or v first
        for iu in xrange(2):
            if iu%2 == 0:
                # loop over x and y directions (using i and j)
                u = uOld + dt*(beta*y*v - g*ddxA(h,dx))
                
            else:
                v = vOld + dt*(-beta*y*u - g*ddyA(h,dy))

        # then calculate h using updated values of u and v
        h = hOld - dt*divA(H*u, H*v, dx, dy)

    return [u,v,h]


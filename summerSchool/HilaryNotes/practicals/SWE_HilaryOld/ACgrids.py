# Functions for calculating gradients and divergences on the A- and C-grids
# and for interpolating variables to different locations for the C-grid and

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
    "Calculates the co-located ddx of 2d array f"
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
    "solves the linearised SWE using forward-backward time-stepping and"
    "the C-grid in a doubly periodic domain starting from u, v and h"
    
    # Derive variables that depend on the inputs
    [nx,ny] = np.shape(u)
    dy = yu[1] - yu[0]
    Hatu = hatu(H*np.ones_like(h)-h0)
    Hatv = hatv(H*np.ones_like(h)-h0)
    
    # loop through all times
    for it in xrange(nt):
        # update old values
        uOld = u.copy()
        vOld = v.copy()
        hOld = h.copy()
        
        # alternate between calculating u or v first
        for iu in xrange(2):
            if (iu+it)%2 == 0:
                # loop over x and y directions (using i and j)
                u = uOld + dt*(beta*yu*vatu(v) - g*ddxC(h+h0, dx))
                
            else:
                v = vOld + dt*(-beta*yv*uatv(u) - g*ddyC(h+h0, dy))

        # then calculate h using updated values of u and v
        h = hOld - dt*divC(Hatu*u, Hatv*v, dx, dy)

    return [u,v,h]


def SWE_Cgrid_nonLin(beta, g, dx, yu, yv, dt, nt, u, v, h, h0):
    "solves the non-linear SWE using forward-backward time-stepping and"
    "the C-grid in a doubly periodic domain starting from u, v and h"
    
    # Derive variables that depend on the inputs
    [nx,ny] = np.shape(u)
    dy = yu[1] - yu[0]
    
    # loop through all times
    for it in xrange(nt):
        # update old values
        uOld = u.copy()
        vOld = v.copy()
        hOld = h.copy()
        
        # alternate between calculating u or v first
        for iu in xrange(2):
            if (iu+it)%2 == 0:
                # loop over x and y directions (using i and j)
                u = uOld + dt*\
                (
                  - u*ddxA(u,dx) - vatu(v)*ddyA(u,dy)
                  + beta*yu*vatu(v) - g*ddxC(h+h0,dx)
                )
                
            else:
                v = vOld + dt*\
                (
                  - uatv(u)*ddxA(v,dx) - v*ddyA(v,dy)
                    -beta*yv*uatv(u) - g*ddyC(h+h0,dy)
                )

        # then calculate h using updated values of u and v
        h = hOld - dt*divC(hatu(h)*u, hatv(h)*v,dx,dy)

    return [u,v,h]


def SWE_Agrid(beta, g, H, dx, y, dt, nt, u, v, h, h0):
    "solves the lienarisedSWE using forward-backward time-stepping and the"
    "A-grid doubly periodic domain stating from u, v and h"
    
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
            if (iu+it)%2 == 0:
                # loop over x and y directions (using i and j)
                u = uOld + dt*(beta*y*v - g*ddxA(h+h0,dx))
                
            else:
                v = vOld + dt*(-beta*y*u - g*ddyA(h+h0,dy))

        # then calculate h using updated values of u and v
        h = hOld - dt*divA((H-h0)*u, (H-h0)*v, dx, dy)

    return [u,v,h]


def SWE_Agrid_nonLin(beta, g, dx, y, dt, nt, u, v, h, h0):
    "solves the non-linear SWE using forward-backward time-stepping and the"
    "A-grid doubly periodic domain stating from u, v and h"
    
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
            if (iu+it)%2 == 0:
                # loop over x and y directions (using i and j)
                u = uOld + dt*\
                (
                  - u*ddxA(u,dx) - v*ddyA(u,dy)
                  + beta*y*v - g*ddxA(h+h0,dx)
                )
                
            else:
                v = vOld + dt*\
                (
                  - u*ddxA(v,dx) - v*ddyA(v,dy)
                    -beta*y*u - g*ddyA(h+h0,dy)
                )

        # then calculate h using updated values of u and v
        h = hOld - dt*divA(h*u, h*v, dx, dy)
        #h = hOld - dt*(h*divA(u, v, dx, dy) + u*ddxA(h,dx) + v*ddyA(h,dy))

    return [u,v,h]


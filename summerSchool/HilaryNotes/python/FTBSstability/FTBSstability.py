from pylab import *
import os

def FTBSstabil(c,kdx):
    "Stability conditions for FTBS"
    return c*(1-c)*(1-cos(kdx))

c = arange(-1,2.1,0.1)

# plots with lines drawn one by one
for iplt in range(5):
    ion()
    clf()
    grid(True, which='both')
    plot(c, zeros(size(c)), 'k--', linewidth=3, label='Stability limit')
    if iplt > 0:
        plot(c, FTBSstabil(c,pi), 'k-', label='$k\Delta x = \pm\pi$')
    if iplt > 1:
        plot(c, FTBSstabil(c,0.5*pi), 'b-', label='$k\Delta x = \pm\pi/2$')
    if iplt > 2:
        plot(c, FTBSstabil(c,0.25*pi), 'g-', label='$k\Delta x = \pm\pi/4$')
    if iplt > 3:
        plot(c, FTBSstabil(c,0), 'r-', label='$k\Delta x = 0$')

    axis([c[0], c[-1],-2,1])

    lgd = legend(bbox_to_anchor=(1.05,1), loc=2, borderaxespad=0.)
    xlabel('$c$')

    font = {'size'   : 20}
    rc('font', **font)

    figName='FTBSstability'+str(iplt+1)+'.pdf'
    plt.savefig(figName, bbox_extra_artists=(lgd,), bbox_inches='tight')



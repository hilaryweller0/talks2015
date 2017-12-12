from pylab import *

# various functions with different total variation, to see the difference
# between total variation and boundedness


x = linspace(0,10,50)
labels = ['(a)', '(b)', '(c)', '(d)', '(e)', '(f)']

# plots with lines drawn one by one
for iplt in range(6):
    ion()
    clf()
    grid(True, axis='y')
    axis([x[0], x[-1],0,7])

    if iplt == 0:
        plot(x, where(abs(x-5)<1, 6, 2), 'k',lw=2)
    if iplt == 1:
        plot(x, 4-2*cos(x*pi/5), 'k',lw=2)
    if iplt == 2:
        plot(x, where(abs(x-3.5)<.5, 1,\
                where(abs(x-5.5)<.5, 7,\
                where(abs(x-4.5)<.5, 6, 2))), 'k',lw=2)
    if iplt == 3:
        plot(x, where(abs(x-3.5)<.5, 4,\
                where(abs(x-5)<1, 6,\
                where(abs(x-6.5)<.5, 4, 2))), 'k',lw=2)
    if iplt == 4:
        plot(x, where(abs(x-3.5)<.2, 3,
                where(abs(x-3.5)<.5, 4,\
                where(abs(x-5)<1, 6,\
                where(abs(x-6.5)<.2, 5,\
                where(abs(x-6.5)<.5, 4, 2))))), 'k',lw=2)
    if iplt == 5:
        plot(x, 3.5-1.5*cos(x*pi/5), 'k',lw=2)

    font = {'size'   : 20}
    rc('font', **font)

    text(0.2, 6.5, labels[iplt])
    #xlabel('$x$')
    ylabel('$\phi$')
    figName='TV'+str(iplt+1)+'.pdf'
    plt.savefig(figName)



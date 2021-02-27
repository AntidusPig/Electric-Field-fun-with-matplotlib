from matplotlib import pyplot as plt
import matplotlib
import numpy as np

'''plt.clabel is not working
color maps of streamplots aren't working as well 
'''

class charge:
    def __init__(self, charge, x, y):
        if charge == 0:
            raise ValueError("Charge doesn't exist")
        self.q = charge
        self.x = x
        self.y = y

def draw_charge(ax, *charges, sizefactor=5e-5):  #size related to charge magnitude
    for q in charges:
        ax.add_artist(plt.Circle((q.x,q.y),q.q*sizefactor,color='#ff0000'if q.q>0else'#0000ff'))

def strength(x,y,*charges,components=False):
    k = 8987551792.261171 # 1/4/math.pi/vacuum electric permittivity
    ex = 0
    ey = 0
    for q in charges:
        ex += q.q/(((q.x-x)**2+(q.y-y)**2)**1.5)*(q.x-x)
        ey += q.q/(((q.x-x)**2+(q.y-y)**2)**1.5)*(q.y-y)
    if components:
        return ex,ey
    return k*np.hypot(ex,ey)

def potential(x,y,*charges):
    k = 8987551792.261171 # 1/4/math.pi/vacuum electric permittivity
    phix = 0
    phiy = 0
    for q in charges:
        phix += q.q/((q.x-x)**2+(q.y-y)**2)*(q.x-x)
        phiy += q.q/((q.x-x)**2+(q.y-y)**2)*(q.y-y)
    return k*np.hypot(phix,phiy)

def draw_field_strength(charges, ax, ignore_factor, cmap=plt.cm.viridis, contours = 8, width=12,height=6):
    fineness = 256
    x_axis, y_axis = np.meshgrid(np.linspace(0-width/2, 0+width/2, fineness), np.linspace(0-height/2, 0+height/2, fineness))
    field_strength = strength(x_axis, y_axis, *charges)
    max = -np.inf
    min = np.inf
    for j in field_strength:
        for i in j:
            if i > max:
                max = i
            elif i < min:
                min = i
    a = (max + min) * ignore_factor  # change the factor[eliminate high values near charge]
    for i in range(field_strength.shape[1]):
        for j in range(field_strength.shape[0]):
            if field_strength[j][i] > a:
                field_strength[j][i] = a
    plt.contourf(x_axis, y_axis, field_strength, contours, alpha=0.75, cmap=cmap)
    C = plt.contour(x_axis, y_axis, field_strength, contours, colors='black', linewidths=.5)
    # plt.clabel(C,inline=True,fontsize=15)
    ax.set_xlabel('$x$')
    ax.set_ylabel('$y$')
    ax.set_xlim(0-width/2, 0+width/2)
    ax.set_ylim(0-height/2, 0+height/2)

def draw_equipotentials(charges, ax, ignore_factor, cmap=plt.cm.viridis, contours = 8, width=12,height=6):
    fineness = 256
    x_axis, y_axis = np.meshgrid(np.linspace(0-width/2, 0+width/2, fineness), np.linspace(0-height/2, 0+height/2, fineness))
    field_potential = potential(x_axis, y_axis, *charges)
    max = -np.inf
    min = np.inf
    for j in field_potential:
        for i in j:
            if i > max:
                max = i
            elif i < min:
                min = i
    a = (max + min) * ignore_factor  # change the factor[eliminate high values near charge]
    for i in range(field_potential.shape[1]):
        for j in range(field_potential.shape[0]):
            if field_potential[j][i] > a:
                field_potential[j][i] = a
    plt.contourf(x_axis, y_axis, field_potential, contours, alpha=0.75, cmap=cmap)
    C = plt.contour(x_axis, y_axis, field_potential, contours, colors='black', linewidths=.5)
    # plt.clabel(C,inline=True,fontsize=15)
    ax.set_xlabel('$x$')
    ax.set_ylabel('$y$')
    ax.set_xlim(0-width/2, 0+width/2)
    ax.set_ylim(0-height/2, 0+height/2)

def draw_fieldlines(charges, ax, cmap=plt.cm.inferno, width=12, height=6, density=1):
    fineness = 256
    x_axis, y_axis = np.meshgrid(np.linspace(0-width/2, 0+width/2, fineness), np.linspace(0-height/2, 0+height/2, fineness))
    ex,ey = strength(x_axis,y_axis,*charges,components=True)
    plt.streamplot(x_axis,y_axis,ex,ey,density=density,cmap=cmap)
    ax.set_xlabel('$x$')
    ax.set_ylabel('$y$')
    ax.set_xlim(0 - width / 2, 0 + width / 2)
    ax.set_ylim(0 - height / 2, 0 + height / 2)

ignore_factor = 0.001  # 靠近电荷数值太高，这是基本的falloff
q1_1 = charge(1000, 1, 0)
q1_2 = charge(-1000, -1, 0)
charges = [q1_1,q1_2]
q2_1 = charge(1000, 1, 0)
q2_2 = charge(1000, -1, 0)
charges2 = [q2_1, q2_2]
q3_1 = charge(1000, 1, 0.5)
q3_2 = charge(800, -1, 0)
q3_3 = charge(1200, 0, -0.6)
charges3 = [q3_1, q3_2, q3_3]
q4_1 = charge(800, 1.5, 0)
q4_2 = charge(-1000, -1.5, 1)
q4_3 = charge(500, 1.5, -1)
q4_4 = charge(1000, -1.5, 0)
charges4 = [q4_1,q4_2,q4_3,q4_4]

matplotlib.rcParams['font.sans-serif'] = ['KaiTi']
matplotlib.rcParams['axes.unicode_minus']=False
a=input('Which demo?(1-3) ')
while a not in ('1','2','3'):
    a=input("... ")
if a=='1':
    fig = plt.figure("electric field")
    ax = fig.add_subplot(221)
    draw_field_strength(charges,ax,ignore_factor,)
    draw_charge(ax, *charges,)

    ax2 = fig.add_subplot(222)
    draw_field_strength(charges2,ax2,ignore_factor,plt.cm.hot)
    draw_charge(ax2, *charges2, )

    ax3 = fig.add_subplot(223)
    draw_field_strength(charges3,ax3,ignore_factor,plt.cm.winter)
    draw_charge(ax3, *charges3, )

    ax4 = fig.add_subplot(224)
    draw_field_strength(charges4,ax4,0.005,plt.cm.jet,16)
    draw_charge(ax4, *charges4, )
elif a=='2':
    fig = plt.figure("electric field")
    ax = fig.add_subplot(221)
    draw_equipotentials(charges, ax, 0.1, )
    draw_charge(ax, *charges, )

    ax2 = fig.add_subplot(222)
    draw_equipotentials(charges2, ax2, 0.05, plt.cm.hot, width=4, height=2)
    draw_charge(ax2, *charges2, )

    ax3 = fig.add_subplot(223)
    draw_equipotentials(charges3, ax3, 0.05, plt.cm.winter, )
    draw_charge(ax3, *charges3, )

    ax4 = fig.add_subplot(224)
    draw_equipotentials(charges4, ax4, 0.01, plt.cm.jet,contours=16)
    draw_charge(ax4, *charges4, )
elif a=='3':
    fig = plt.figure("electric field")
    ax = fig.add_subplot(221)
    draw_fieldlines(charges, ax)
    draw_charge(ax, *charges, )

    ax2 = fig.add_subplot(222)
    draw_fieldlines(charges2, ax2, plt.cm.hot, height=2, width=4)
    draw_charge(ax2, *charges2, )

    ax3 = fig.add_subplot(223)
    draw_fieldlines(charges3, ax3, plt.cm.winter, density=1.5)
    draw_charge(ax3, *charges3, )

    ax4 = fig.add_subplot(224)
    draw_fieldlines(charges4, ax4, cmap=plt.cm.jet, density=1.5)
    draw_charge(ax4, *charges4, )

plt.show()
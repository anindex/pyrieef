from demos_common_imports import *
import numpy as np
from scipy.interpolate import RectBivariateSpline
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from geometry.differentiable_geometry import *
import math


class ExpF(DifferentiableMap):

    def __init__(self):
        return

    def output_dimension(self):
        return 1

    def input_dimension(self):
        return 2

    def forward(self, p):
        assert p.size == 2
        return math.exp(-(2 * p[0])**2 - (p[1] / 2)**2)

# Regularly-spaced, coarse grid
dx, dy = 0.4, 0.4
xmax, ymax = 2, 4
x = np.arange(-xmax, xmax, dx)
y = np.arange(-ymax, ymax, dy)
X, Y = np.meshgrid(x, y)
Z = np.exp(-(2 * X)**2 - (Y / 2)**2)
print Z.shape

interp_spline = RectBivariateSpline(x, y, Z.transpose())

# Regularly-spaced, fine grid
dx2, dy2 = 0.16, 0.16
x2 = np.arange(-xmax, xmax, dx2)
y2 = np.arange(-ymax, ymax, dy2)
Z2 = interp_spline(x2, y2, dx=0, dy=0)
g2 = interp_spline(x2, y2, dx=1, dy=1)

f = ExpF()
g1_x = np.zeros((x2.size, y2.size))
g1_y = np.zeros((x2.size, y2.size))
z1 = np.zeros((x2.size, y2.size))
print "g1 : ", g1_x.shape
for i, x in enumerate(x2):
    for j, y in enumerate(y2):
        p = np.array([x, y])
        z1[i, j] = f.forward(p)
        grad = f.gradient(p)
        g1_x[i, j] = grad[0]
        g1_y[i, j] = grad[1]


print "Z2 : ", Z2.shape
print "g2 : ", g2.shape

print "Z2 : ", Z2
# print "g2 : ", g2
# print "g1_x : ", g1_x
# print "g1_y : ", g1_y
print "z1 : ", z1


X2, Y2 = np.meshgrid(x2, y2)

fig, ax = plt.subplots(nrows=1, ncols=3, subplot_kw={'projection': '3d'})
ax[0].plot_wireframe(X, Y, Z, color='k')
ax[1].plot_wireframe(X2, Y2, Z2.transpose(), color='k')
ax[2].plot_wireframe(X2, Y2, z1.transpose(), color='k')
for axes in ax:
    axes.set_zlim(-0.2, 1)
    axes.set_axis_off()

fig.tight_layout()
plt.show()

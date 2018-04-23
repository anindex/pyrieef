#!/usr/bin/env python

# Copyright (c) 2015 Max Planck Institute
# All rights reserved.
#
# Permission to use, copy, modify, and distribute this software for any purpose
# with or without   fee is hereby granted, provided   that the above  copyright
# notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
# REGARD TO THIS  SOFTWARE INCLUDING ALL  IMPLIED WARRANTIES OF MERCHANTABILITY
# AND FITNESS. IN NO EVENT SHALL THE AUTHOR  BE LIABLE FOR ANY SPECIAL, DIRECT,
# INDIRECT, OR CONSEQUENTIAL DAMAGES OR  ANY DAMAGES WHATSOEVER RESULTING  FROM
# LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
# OTHER TORTIOUS ACTION,   ARISING OUT OF OR IN    CONNECTION WITH THE USE   OR
# PERFORMANCE OF THIS SOFTWARE.
#
#                                           Jim Mainprice on Sunday June 17 2017

import demos_common_imports
import numpy as np
import matplotlib.pyplot as plt
from workspace import *
from charge_simulation import *
from pixel_map import *
from geodesics import *
import itertools

workspace = Workspace()
workspace.AddCircle(np.array([0.1, .3]), .1)
workspace.AddCircle(np.array([0., -.3]), .1)
points = workspace.AllPoints()
X = np.array(points)[:,0]
Y = np.array(points)[:,1]

simulation = ChargeSimulation()
simulation.charged_points_ = points
simulation.Run()

extends = Extends(workspace.box.dim[0]/2.)
grid = PixelMap(0.01, extends)
matrix = np.zeros((grid.nb_cells_x, grid.nb_cells_y))
for i in range(grid.nb_cells_x):
    for j in range(grid.nb_cells_y):
        p = grid.grid_to_world(np.array([i, j]))
        # TODO why is it this way... (j before i)
        # these are matrix coordinates...
        matrix[j, i] = simulation.PotentialCausedByObject(p)
plt.imshow(matrix, origin='lower',extent=workspace.box.Extends())
plt.scatter( X, Y )
plt.ylabel('some points')
plt.axis('equal')
plt.axis(workspace.box.Extends())

x_goal = np.array([0.4, 0.2])
nx, ny = (10, 5)
x = np.linspace(.5, -.5, nx)
y = np.linspace(-.5, -.2, ny)
for i, j in itertools.product(range(nx), range(ny)):
    x_init = np.array([x[i], y[j]])
    line = ComputeGeodesic(simulation, x_init, x_goal)
    X = np.array(line)[:,0]
    Y = np.array(line)[:,1]
    plt.plot( X, Y, color="r", linewidth=2.0 )
    plt.plot( x_init[0], x_init[1], 'ro' )
plt.plot( x_goal[0], x_goal[1], 'ko' )
plt.show()  


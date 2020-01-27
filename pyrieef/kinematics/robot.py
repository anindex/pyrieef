#!/usr/bin/env python

# Copyright (c) 2020, University of Stuttgart
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
#                                    Jim Mainprice on Friday January 23 2020

from abc import abstractmethod
from .homogeneous_transform import *
import json
import os


class Robot:
    """
    Abstract robot class
    """

    def __init__(self):
        self.name = None
        self.shape = None
        self.keypoints = None
        self._maps = []

    @abstractmethod
    def forward_kinematics_map(self):
        raise NotImplementedError()


class Freeflyer(Robot):
    """
    Planar 3DoFs robot
    """

    def __init__(self, keypoints=[0., 0.]):
        Robot.__init__(self)

    def keypoint_map(self, i):
        return self._maps[i]

    def _create_maps(self, keypoints):
        for p in keypoints:
            self._maps.append(HomogeneousTransform(p))


def assets_data_dir():
    return os.path.abspath(os.path.dirname(__file__)) + os.sep + "../../data"


def create_robot_from_file(filename=assets_data_dir() + "/freeflyer.json"):
    print(filename)
    with open(filename, "r") as read_file:
        config = json.loads(read_file.read())
        robot = Freeflyer(None)
        robot.name = config["name"]
        # robot.name = config.name
        # robot.shape = config.contour
    return robot

"""Script that make an arrow that is drawn and can be rotated to indicate direction.
"""

import math
import numpy as np
import pygame

import config as cf
from precode2 import ReturnZero, Vector2D


class Arrow:
    """Make an arrow that can be drawn, displayed and rotated.
    """

    def __init__(self):
        """Initializing all attributes 'Arrow' needs.
        """
        self.pos = Vector2D(cf.X_POS, cf.Y_POS)
        # To the 'north'
        self.dir = Vector2D(0, -1)
        self.vel = 0.0
        self.two_d_pos = Vector2D(0, 0)

    def draw(self, screen):
        """Draw a polygon that takes the shape of a big arrow.

        Makes the polygon from seven 'Vector2D' objects that are all based on the 'dir'-attribute of the arrow.

        Arguments:
            screen {pygame surface} -- the surface that the polygon shall be drawn onto
        """
        try:
            # Every point is rotated from 'dir' about the center of the polygon,
            # and are then scaled out to give it the correct shape of an arrow.
            one = self.dir.rotate(
                cf.ROTATION[0]).normalized() * cf.SCALING[0]
            two = self.dir.rotate(
                cf.ROTATION[1]).normalized() * cf.SCALING[1]
            three = self.dir.rotate(
                cf.ROTATION[2]).normalized() * cf.SCALING[2]
            four = self.dir.rotate(
                cf.ROTATION[3]).normalized() * cf.SCALING[3]
            five = self.dir.rotate(
                cf.ROTATION[4]).normalized() * cf.SCALING[4]
            six = self.dir.rotate(
                cf.ROTATION[5]).normalized() * cf.SCALING[5]
            seven = self.dir.rotate(
                cf.ROTATION[6]).normalized() * cf.SCALING[6]
            pygame.draw.polygon(screen, (cf.POLYGON_COLOR),
                                ((self.pos.x + one.x, self.pos.y + one.y),
                                 (self.pos.x + two.x, self.pos.y + two.y),
                                 (self.pos.x + three.x, self.pos.y + three.y),
                                 (self.pos.x + four.x, self.pos.y + four.y),
                                 (self.pos.x + five.x, self.pos.y + five.y),
                                 (self.pos.x + six.x, self.pos.y + six.y),
                                 (self.pos.x + seven.x, self.pos.y + seven.y)))
        except ReturnZero:
            # In case we try to normalize a null-vector,
            # e.g. if 'dir' has a length of zero.
            one = Vector2D(0, 0)
            two = Vector2D(0, 0)
            three = Vector2D(0, 0)
            four = Vector2D(0, 0)
            five = Vector2D(0, 0)
            six = Vector2D(0, 0)
            seven = Vector2D(0, 0)

    def globe_motion(self, earth, NS, EW, dot_y, dot_x):
        """Make the movement fit to a globe Earth, where straight lines
        are great circles and not straight lines in Euclidean space.
        """
        try:
            direction = self.dir.rotate(90)
            angle = math.degrees(np.arctan2(direction.y, direction.x))
            p = earth.Direct(NS, EW, angle, self.vel)
            rotation = p['azi2'] - p['azi1']
            self.dir = self.dir.rotate(rotation)
            self.two_d_pos.y -= p['lat2'] - p['lat1']
            dot_y -= p['lat2'] - p['lat1']
            self.two_d_pos.x += p['lon2'] - p['lon1']
            dot_x += p['lon2'] - p['lon1']
            NS, EW = p['lat2'], p['lon2']
        except Exception:
            pass

        return NS, EW, dot_y, dot_x

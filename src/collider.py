################################################################################
################################################################################
#
# collider.py
#
# This file contains all of the physics implementations used in our game. Mostly,
# this is just a game object in the world that contains a bounding box that we
# can test against.
#
################################################################################

import pygame

from lib.euclid import *
from gameobject import *
from utils import *

class Collider(GameObject):
    def __init__(self, pos, width, height, angle):
        super(Collider, self).__init__()
        self.pos = pos
        self.angle = angle
        
        diag = Vector2(width * 0.5, height * 0.5)
        self.aabb.removeAll()
        self.aabb.add_point(pos - diag)
        self.aabb.add_point(pos + diag)
        self.colliding = False

    def getPoints(self):
        pts = self.aabb.getPoints()

        pts = map(lambda x: x - self.pos, pts)
        pts = map(lambda x: x.rotateDeg(self.angle), pts)
        pts = map(lambda x: self.pos + x, pts)

        return pts

    def collide(self, obj):
        
        # Rotate all the points of the colliders so that
        # this collider lines up with the x/y axes
        pts = obj.aabb.getPoints()

        pts = map(lambda x: x - self.pos, pts)
        pts = map(lambda x: x.rotateDeg(-self.angle), pts)
        pts = map(lambda x: self.pos + x, pts)

        self.colliding = self.aabb.collidePolygon(pts)
        return self.colliding

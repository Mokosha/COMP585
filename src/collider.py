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
    DEBUG = False
    
    def __init__(self, pos, width, height, angle):
        super(Collider, self).__init__()
        self.pos = pos
        self.angle = angle
        
        diag = Vector2(width * 0.5, height * 0.5)
        self.aabb.add_point(pos - diag)
        self.aabb.add_point(pos + diag)

    def render(self, surface, campos):
        if Collider.DEBUG:
            pts = self.aabb.getPoints()

            pts = map(lambda x: x - self.pos, pts)
            pts = map(lambda x: x.rotateDeg(self.angle), pts)
            pts = map(lambda x: x + self.pos, pts)
            pts = map(lambda x: world2screenPos(campos, x), pts)

            c = pygame.Color(255, 128, 128, 255)
            pygame.draw.polygon(surface, c, pts, 2)

    def testAgainst(self, collider):
        
        # Rotate all the points of the colliders so that
        # this collider lines up with the x/y axes
        pts = collider.getPoints()

        pts = map(lambda x: x - self.pos, pts)
        pts = map(lambda x: x.rotateDeg(-self.angle), pts)
        pts = map(lambda x: self.pos + x, pts)

        return self.aabb.collidePolygon(pts)

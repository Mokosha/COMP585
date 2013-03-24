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

class Collider(GameObject):
    DEBUG = False
    
    def __init__(self, pos, width, height, angle):
        super(Collider, self).__init__()
        self.pos = pos
        self.angle = angle
        
        diag = Vector2(width * 0.5, height * 0.5)
        self.aabb.add_point(pos - diag)
        self.aabb.add_point(pos + diag)

    def render(self, time, surface, campos):
        if Collider.DEBUG:
            left = world2screen(self.aabb.minval.x)
            top = world2screen(self.aabb.maxval.y)
            width = world2screen(self.aabb.maxx() - self.aabb.minx())
            height = world2screen(self.aabb.maxy() - self.aabb.miny())
            r = pygame.Rect(left, top, width, height)
            pygame.draw.rect(surface, pygame.color(1.0, 0.5, 0.5), r, 2)
            

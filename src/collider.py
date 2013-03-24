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
    DEBUG = True
    
    def __init__(self, pos, width, height, angle):
        super(Collider, self).__init__()
        self.pos = pos
        self.angle = angle
        
        diag = Vector2(width * 0.5, height * 0.5)
        self.aabb.add_point(pos - diag)
        self.aabb.add_point(pos + diag)

    def render(self, time, surface, campos):
        if Collider.DEBUG:
            topleft = Vector2(self.aabb.minval.x, self.aabb.maxval.y)
            left = world2screenPos(campos, topleft).x
            top = world2screenPos(campos, topleft).y
            width = world2screen(self.aabb.maxx() - self.aabb.minx())
            height = world2screen(self.aabb.maxy() - self.aabb.miny())
            r = pygame.Rect(left, top, width, height)
            c = pygame.Color(255, 128, 128, 255)
            pygame.draw.rect(surface, c, r, 2)
            

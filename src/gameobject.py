################################################################################
################################################################################
#
# gameobject.py
#
# This file contains the base implementation for all of the game objects in the
# game. Game objects are objects that conform to a certain set of rules:
# 
# 1. They have a position and orientation
# 2. They can be drawn
# 3. They can respond to input events
#
################################################################################

import pygame

from lib.euclid import *

class AABoundingBox:
    def __init__(self):
        self.minval = Vector2(0, 0)
        self.maxval = Vector2(0, 0)

    def maxx(self):
        return self.maxval.x

    def maxy(self):
        return self.maxval.y

    def minx(self):
        return self.minval.x

    def miny(self):
        return self.minval.y

    def center(self):
        return 0.5 * (self.maxval + self.minval)

    def add_point(self, point):
        self.maxval.x = max(self.maxx(), point.x)
        self.maxval.y = max(self.maxy(), point.y)
        self.minval.x = min(self.minx(), point.x)
        self.minval.y = min(self.miny(), point.y)

    def collide(self, point):
        collision = True
        collision = collision and point.y > self.minval.y and point.y < self.maxval.y
        collision = collision and point.x > self.minval.x and point.x < self.maxval.x
        return collision

    def collide(self, box):
        if(box.minx() > self.maxx()):
            return False
        if(box.maxx() < self.minx()):
            return False
        if(box.miny() > self.maxy()):
            return False
        if(box.maxy() < self.miny()):
            return False

        return True

class GameObject(object):

    def getpos(self):
        return self.__pos

    def setpos(self, newpos):
        self.__pos = newpos

    def delpos(self):
        del self.__pos

    pos = property(getpos, setpos, delpos, "World space position of this game object")

    def __init__(self):
        super(GameObject, self).__init__()
        self.pos = Vector2(0, 0)
        self.angle = 0
        self.aabb = AABoundingBox()

    def render(self, time, surface, campos):
        pass

    def accept(self, event):
        pass

    def collide(self, box):
        return self.aabb.collide(box)

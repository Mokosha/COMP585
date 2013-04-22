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

import pygame, sys

from lib.euclid import *
from utils import *

class AABoundingBox:
    def __init__(self):
        self.removeAll()

    def removeAll(self):
        self.minval = Vector2(sys.float_info.max, sys.float_info.max)
        self.maxval = Vector2(-sys.float_info.max, -sys.float_info.max)        

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

    def collidePoint(self, point):
        collision = True
        collision = collision and point.y > self.minval.y and point.y < self.maxval.y
        collision = collision and point.x > self.minval.x and point.x < self.maxval.x
        return collision

    def collideBox(self, box):
        if(box.minx() > self.maxx()):
            return False
        if(box.maxx() < self.minx()):
            return False
        if(box.miny() > self.maxy()):
            return False
        if(box.maxy() < self.miny()):
            return False

        return True

    def getPoints(self):
        pts = [self.minval]
        pts.append(Vector2(self.maxval.x, self.minval.y))
        pts.append(self.maxval)
        pts.append(Vector2(self.minval.x, self.maxval.y))
        return pts

    # Assume that the polygon is simply a list of vertices, and simply
    # do a SAT on it...
    def collidePolygon(self, polygon):

        if len(polygon) == 0:
            return False

        if self.collidePoint(polygon[0]):
            return True

        if len(polygon) == 1:
            return False

        def testSides(polyA, polyB):

            pt1 = polyA[0]
            for i in range(1, len(polyA)+1):
                idx = i % len(polyA)
                pt2 = polyA[idx]

                # Project all points to the line perpendicular to this edge
                yAxis = (pt1 - pt2).normalized()
                xAxis = yAxis.rotateDeg(-90)

                trpts = map(lambda x: x - pt2, polyB)
                if all(map(lambda x: x.dot(xAxis) < 0, trpts)):
                    return False

                pt1 = pt2

            return True

        boxpts = self.getPoints()
        collision = testSides(polygon, boxpts) and testSides(boxpts, polygon)
        return collision

class GameObject(object):

    DEBUG = False

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
        self.aabb.add_point(self.pos)

        self.dynamic = False
        self.zone = -1

    def render(self, surface, campos):
        if GameObject.DEBUG:

            pts = self.aabb.getPoints()

            pts = map(lambda x: x - self.pos, pts)
            pts = map(lambda x: x.rotateDeg(self.angle), pts)
            pts = map(lambda x: x + self.pos, pts)
            pts = map(lambda x: world2screenPos(campos, x), pts)

            c = pygame.Color(255, 128, 128, 255)
            pygame.draw.polygon(surface, c, pts, 2)

    def accept(self, event):
        pass

    def process(self, dt):
        pass

    def collide(self, obj):
        return False

class Sprite(GameObject):
    def __init__(self, world_pos, fname, width = None, height = None):
        super(Sprite, self).__init__()
        self.isurf = pygame.image.load(getRootPath() + os.sep + "assets" + os.sep + fname)
        aspect = float(self.isurf.get_width()) / float(self.isurf.get_height())
        self.pos = world_pos

        if width != None or height != None:
            if width != None:
                self.screenwidth = int(world2screen(width))
                if height == None:
                    self.screenheight = int(self.screenwidth / aspect)

            if height != None:
                self.screenheight = int(world2screen(height))
                if width == None:
                    self.screenwidth = int(self.screenheight * aspect)

            self.isurf = pygame.transform.scale(self.isurf,(self.screenwidth, self.screenheight))
        else:
            self.screenwidth = self.isurf.get_width()
            self.screenheight = self.isurf.get_height()

    def render(self, surface, campos):

        screenpos = world2screenPos(campos, self.pos)
        screenpos.y -= (self.screenheight / 2)
        screenpos.x -= (self.screenwidth / 2)

        surface.blit(self.isurf, screenpos)


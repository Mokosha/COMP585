################################################################################
################################################################################
#
# utils.py
#
# This file contains all of the utility functions associated with the game. These
# methods are used all throughout the source but don't really belong to any 
# specific module...
#
################################################################################

import math, os
from lib.euclid import *

#
# Math
#
def lerp(a, b, t):
    return (1.0 - t)*a + t*b

def smoothstep(a, b, t):
    t = t * t * (3.0 - (2.0 * t))
    return lerp(a, b, t)

def polar2cart(angle, dist):

    angle *= math.pi / 180.0
    x = dist * math.cos(angle)
    y = dist * math.sin(angle)

    return Vector2(x, -y)

def clamp(a, low, high):
    return max(low, min(a, high))

def lineSegIntersect(l1, l2):
    
    # Parametric representation
    A, B = l1[0], l1[1]
    C, D = l2[0], l2[1]

    BmA = B - A
    BmA3 = Vector3(BmA.x, BmA.y, 0)

    DmC = D - C
    DmC3 = Vector3(DmC.x, DmC.y, 0)

    A3 = Vector3(A.x, A.y, 0)
    B3 = Vector3(B.x, B.y, 0)
    C3 = Vector3(C.x, C.y, 0)
    D3 = Vector3(D.x, D.y, 0)

    if BmA3.cross(D3 - A3).dot(BmA3.cross(C3 - A3)) >= 0:
        return False

    if DmC3.cross(A3 - C3).dot(DmC3.cross(B3 - C3)) >= 0:
        return False

    return True

#
# Logistics
#
def getRootPath():
    root_path = os.path.realpath(__file__).split(os.sep)[:-2]
    return os.sep.join(root_path)

#
# Camera 
#
WORLD_TO_SCREEN = 100.0

def world2screen(x):
    return x * WORLD_TO_SCREEN

def screen2world(x):
    return x / WORLD_TO_SCREEN

def screenSizeX():
    return 800

def screenSizeY():
    return 600

def world2screenPos(camPos, pos):
    screenPos = world2screen(pos - camPos)
    
    # Since the screen's coordinate system starts from the top
    # left and ours starts from the bottom left, we need to subtract
    # the computed screen position from the screen size...
    return Vector2(screenPos.x, screenSizeY() - screenPos.y)

def screen2worldPos(camPos, pos):
    screenPos = screen2world(Vector2(pos.x, screenSizeY() - pos.y))
    return screenPos - camPos


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

def polar2cart(angle, dist):

    angle *= math.pi / 180.0
    x = dist * math.cos(angle)
    y = dist * math.sin(angle)

    return Vector2(x, -y)

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


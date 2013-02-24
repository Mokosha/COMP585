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

import math
from lib.euclid import *

def lerp(a, b, t):
	return (1.0 - t)*a + t*b

def polar2cart(angle, dist):

	angle = (90 - angle) * math.pi / 180
	x = dist * math.cos(angle)
	y = dist * math.sin(angle)

	return Vector2(x, -y)

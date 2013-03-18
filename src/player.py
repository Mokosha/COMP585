################################################################################
################################################################################
#
# player.py
#
# This file contains all of the logic associated with a given player. It will
# contain their current color and perform any movement and action associated with it.
#
################################################################################

import pygame, os, time
import animation
from animatedobject import *
from utils import *

class Player(AnimatedObject):

    def __init__(self):
        super(Player, self).__init__("smooth-idle")
        self.startAnimation("smooth-idle", time.clock())

        # Initially start in the middle of the screen.
        self.pos = screen2worldPos(Vector2(0, 0), 0.5 * Vector2(screenSizeX(), screenSizeY()))



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
from eventmanager import Events, InputManager
from animatedobject import *
from utils import *

class Player(AnimatedObject):

    def __init__(self):
	
	self.currentColor = pygame.color.Color("white")
        super(Player, self).__init__("smooth-idle")
        self.startAnimation("smooth-idle", time.clock())

        # Initially start in the middle of the screen.
        self.pos = screen2worldPos(Vector2(0, 0), 0.5 * Vector2(screenSizeX(), screenSizeY()))

    def update(self, inputManager):
        if inputManager.isCurrentEvent(Events.MOVE_LEFT):
            #move left
            pass
        elif inputManager.isCurrentEvent(Events.MOVE_RIGHT):
            #move right
            pass
	elif inputManager.isCurrentEvent(Events.CHANGE_COLOR_1):
		self.currentColor = pygame.color.Color("red")
		print(self.currentColor)
	elif inputManager.isCurrentEvent(Events.CHANGE_COLOR_2):
		self.currentColor = pygame.color.Color("green")
		print(self.currentColor)
	elif inputManager.isCurrentEvent(Events.CHANGE_COLOR_3):
		self.currentColor = pygame.color.Color("blue")
		print(self.currentColor)
	elif inputManager.isCurrentEvent(Events.RESET_COLOR):
		self.currentColor = pygame.color.Color("white")
		print(self.currentColor)
		

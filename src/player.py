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
import math, re
import animation
from eventmanager import Events, InputManager
from animatedobject import *
from utils import *

class Player(AnimatedObject):

    def __init__(self):

	self.currentColor = pygame.color.Color("black")
        super(Player, self).__init__("smooth-idle", True)
        self.startAnimation("smooth-idle", time.time())

        # Initially start in the middle of the screen.
        self.pos = screen2worldPos(Vector2(0, 0), 0.5 * Vector2(screenSizeX(), screenSizeY()))


    def changeColor(self,toChangeColor):
	myAnimations = self.animations
	idleAnimation = myAnimations["smooth-idle"]
	myLimb = idleAnimation.limb
	self.iterateChangeColor(myLimb, toChangeColor)
	
	
    def iterateChangeColor(self, limb, toChangeColor):
	animationKeys = limb.attribs['colour'].animationKeys
	for keyframe in animationKeys.keys():
		animationKeys[keyframe] = Vector3(toChangeColor.r,toChangeColor.g,toChangeColor.b)
	if limb.children:
		for child in limb.children:
			self.iterateChangeColor(child, toChangeColor)


    def update(self, inputManager):
        if inputManager.isCurrentEvent(Events.MOVE_LEFT):
            #move left
            pass
        elif inputManager.isCurrentEvent(Events.MOVE_RIGHT):
            #move right
            pass
	elif inputManager.isCurrentEvent(Events.CHANGE_COLOR_1):
		if (self.currentColor.r == 0):
			self.currentColor = pygame.color.Color(128, self.currentColor.g, self.currentColor.b)
		elif (self.currentColor.r == 128):
			self.currentColor = pygame.color.Color(255, self.currentColor.g, self.currentColor.b)
		self.changeColor(self.currentColor)
	elif inputManager.isCurrentEvent(Events.CHANGE_COLOR_2):
		if (self.currentColor.g == 0):
			self.currentColor = pygame.color.Color(self.currentColor.r, 128, self.currentColor.b)
		elif (self.currentColor.g == 128):
			self.currentColor = pygame.color.Color(self.currentColor.r, 255, self.currentColor.b)
		self.changeColor(self.currentColor)
	elif inputManager.isCurrentEvent(Events.CHANGE_COLOR_3):
		if (self.currentColor.b == 0):
			self.currentColor = pygame.color.Color(self.currentColor.r, self.currentColor.g, 128)
		elif (self.currentColor.b == 128):
			self.currentColor = pygame.color.Color(self.currentColor.r, self.currentColor.g, 255)
		self.changeColor(self.currentColor)
	elif inputManager.isCurrentEvent(Events.RESET_COLOR):
		self.currentColor = pygame.color.Color("black")
		self.changeColor(self.currentColor)

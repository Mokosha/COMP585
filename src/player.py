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
        self.loadAnim("walk", True)

        # Initially start in the middle of the screen.
        self.pos = screen2worldPos(Vector2(0, 0), 0.5 * Vector2(screenSizeX(), screenSizeY()))

        self.x = screenSizeX()
        self.y = screenSizeY()
        self.velocity = 0
        self.yGravity = 2
        self.yVelocity = 5
		
    def getX(self):
        return self.x

    def setX(self, value):
        self.x = value	

    def setY(self, value):
        self.y = value
		
    def getY(self):
        return self.y
	
    def getVelocity(self):
        return self.velocity
	
    def setVelocity(self, value):
        self.velocity = value

    def changeColor(self,toChangeColor):
	myLimb = self.currentAnim.limb
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
            x = self.getX() - 15
            y = self.getY()
            self.setX(x)
            self.pos = screen2worldPos(Vector2(0, 0), 0.5 * Vector2(x , y))

            self.startAnimation("walk", time.time())

        if inputManager.isCurrentEvent(Events.MOVE_RIGHT):
            x = self.getX() + 15
            y = self.getY()
            self.setX(x)
            self.pos = screen2worldPos(Vector2(0, 0), 0.5 * Vector2(x , y))

            self.startAnimation("walk", time.time())

        if inputManager.isCurrentEvent(Events.JUMP):
            #if on ground/ground hitbox
            #if self.getY().collides()?:
            if self.velocity == 0:
                self.setVelocity(300)
            else:
                self.setVelocity(0)
	if inputManager.isCurrentEvent(Events.CHANGE_COLOR_1):
		if (self.currentColor.r == 0):
			self.currentColor = pygame.color.Color(128, self.currentColor.g, self.currentColor.b)
		elif (self.currentColor.r == 128):
			self.currentColor = pygame.color.Color(255, self.currentColor.g, self.currentColor.b)
		self.changeColor(self.currentColor)
	if inputManager.isCurrentEvent(Events.CHANGE_COLOR_2):
		if (self.currentColor.g == 0):
			self.currentColor = pygame.color.Color(self.currentColor.r, 128, self.currentColor.b)
		elif (self.currentColor.g == 128):
			self.currentColor = pygame.color.Color(self.currentColor.r, 255, self.currentColor.b)
		self.changeColor(self.currentColor)
	if inputManager.isCurrentEvent(Events.CHANGE_COLOR_3):
		if (self.currentColor.b == 0):
			self.currentColor = pygame.color.Color(self.currentColor.r, self.currentColor.g, 128)
		elif (self.currentColor.b == 128):
			self.currentColor = pygame.color.Color(self.currentColor.r, self.currentColor.g, 255)
		self.changeColor(self.currentColor)
	if inputManager.isCurrentEvent(Events.RESET_COLOR):
		self.currentColor = pygame.color.Color("black")
		self.changeColor(self.currentColor)

    def gravity(self):
        #if not on ground/ground hitbox
        if self.getY() < screenSizeY():
            y = self.getY() + self.yGravity
            x = self.getX()
            self.setY(y)
            self.pos = screen2worldPos(Vector2(0, 0), 0.5 * Vector2(x , y))
            if self.getVelocity() > 0:
                self.setVelocity(self.getVelocity() - 2)

			
    def jump(self):
        #constant velocity...velocity should probably be renamed to jumpTime or something. yVelocity is the velocity of the jump per clock cycle. 
        if self.velocity != 0:
            y = self.getY() - self.yVelocity
            x = self.getX()
            self.setY(y)
            self.pos = screen2worldPos(Vector2(0, 0), 0.5 * Vector2(x , y))

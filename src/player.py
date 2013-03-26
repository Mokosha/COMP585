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
        super(Player, self).__init__("smooth-idle")
        self.startAnimation("smooth-idle", time.clock())

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
		
    def update(self, inputManager):
        if inputManager.isCurrentEvent(Events.MOVE_LEFT):
            x = self.getX() - 15
            y = self.getY()
            self.setX(x)
            self.pos = screen2worldPos(Vector2(0, 0), 0.5 * Vector2(x , y))
        elif inputManager.isCurrentEvent(Events.MOVE_RIGHT):
            x = self.getX() + 15
            y = self.getY()
            self.setX(x)
            self.pos = screen2worldPos(Vector2(0, 0), 0.5 * Vector2(x , y))
        elif inputManager.isCurrentEvent(Events.JUMP):
            #if on ground/ground hitbox
            #if self.getY().collides()?:
            if self.velocity == 0:
                self.setVelocity(300)
            else:
                self.setVelocity(0)
			
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
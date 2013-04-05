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
from collider import *

# Simple game object that we put in our level definition files to figure out
# where to load the player in each zone...
class PlayerStartGizmo(GameObject):
    def __init__(self):
        super(PlayerStartGizmo, self).__init__()

class Player(AnimatedObject):

    MOVE_SPEED_X = 2.0
    INITIAL_JUMP = 10.0
    ACCELERATION = Vector2(0,-9.8)

    def __init__(self):

        self.currentColor = pygame.color.Color("black")
        super(Player, self).__init__("smooth-idle", True)
        self.loadAnim("walk", True)

        # Initially start in the middle of the screen.
        self.pos = screen2worldPos(Vector2(0, 0), 0.5 * Vector2(screenSizeX(), screenSizeY()))
        self.vel = Vector2(0,0)
        self.acc = Player.ACCELERATION

        self.collidedLastFrame = False

        self.velocity = 0
        self.yGravity = 2
        self.yVelocity = 5
        self.dynamic = True
	
    def getVelocity(self):
        return self.velocity
	
    def setVelocity(self, value):
        self.velocity = value

    def changeColor(self,toChangeColor):
	myLimb = self.currentAnim.limb
        self.color = self.currentColor

    def update(self, inputManager):

        if inputManager.isCurrentEvent(Events.MOVE_LEFT):
            self.vel = Vector2(-Player.MOVE_SPEED_X,0)
            self.startAnimation("walk", time.time())

        if inputManager.isCurrentEvent(Events.MOVE_RIGHT):
            self.vel = Vector2(Player.MOVE_SPEED_X,0)
            self.startAnimation("walk", time.time())

        if inputManager.isCurrentEvent(Events.JUMP):
            self.vel = Vector2(0, Player.INITIAL_JUMP)

        if inputManager.debounceEvent(Events.CHANGE_COLOR_1):
            self.currentColor.r = min(self.currentColor.r + 128, 255)
            self.changeColor(self.currentColor)

        if inputManager.debounceEvent(Events.CHANGE_COLOR_2):
            self.currentColor.g = min(self.currentColor.g + 128, 255)
            self.changeColor(self.currentColor)

        if inputManager.debounceEvent(Events.CHANGE_COLOR_3):
            self.currentColor.b = min(self.currentColor.b + 128, 255)
            self.changeColor(self.currentColor)

        if inputManager.debounceEvent(Events.RESET_COLOR):
            self.currentColor = pygame.color.Color("black")
            self.changeColor(self.currentColor)
                
        if len(inputManager.getCurrentEvents()) == 0:
            self.startAnimation("smooth-idle", time.time())
            self.vel = Vector2(0,0)

    def collide(self, obj):        
        
        if isinstance(obj, Collider) and obj.collide(self):
            
            # !FIXME! Assume that the player aabb corners are within the collider...
            objx = Vector2(1, 0).rotateDeg(obj.angle)
            objy = Vector2(0, 1).rotateDeg(obj.angle)

            objw = obj.aabb.maxval.x - obj.aabb.minval.x
            objh = obj.aabb.maxval.y - obj.aabb.minval.y

            # !FIXME! ... really
            self.vel = Vector2(0, 0)
            self.acc = Vector2(0, 0)
            self.collidedLastFrame = True

    def process(self, dt): 
        self.vel += self.acc * dt	
        self.pos += self.vel * dt

        if self.collidedLastFrame:
            self.acc = Player.ACCELERATION

        self.collidedLastFrame = False

        super(Player, self).process(dt)

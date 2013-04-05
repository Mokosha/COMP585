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

    def colliderResponse(self, collider):

        n = (-self.vel).normalized()
        pts = self.aabb.getPoints()

        anchor = None
        for pt in self.aabb.getPoints():

            behind = any(map(lambda x: (x - pt).dot(n) < 0, pts))
            if not behind:
                anchor = pt
                break

        cpts = collider.getPoints()
        canchor = None
        for pt in cpts:
            behind = all(map(lambda x: (x - pt).dot(n) < 0, [p for p in cpts if not p is pt]))
            if behind:
                canchor = pt
                break

        # !FIXME! This assumes that the player and collider are both OBBs
        lowerShell = []
        for i in range(len(pts)):
            A = pts[i]
            B = pts[(i+1) % len(pts)]
            C = pts[(i+2) % len(pts)]

            if B is anchor:
                lowerShell = [A, B, C]
                break

        upperShell = []
        for i in range(len(cpts)):
            A = cpts[i]
            B = cpts[(i+1) % len(cpts)]
            C = cpts[(i+2) % len(cpts)]

            if B is canchor:
                upperShell = [A, B, C]
                break

        # convert both shells to new coordinate system
        yAxis = n
        xAxis = n.rotateDeg(-90)

        lowerShell = map(lambda v: Vector2(v.dot(xAxis), v.dot(yAxis)), lowerShell)
        upperShell = map(lambda v: Vector2(v.dot(xAxis), v.dot(yAxis)), upperShell)

        lowerShell = sorted(lowerShell, key=lambda v: v.x)
        upperShell = sorted(upperShell, key=lambda v: v.x)

        class ShellPt:
            def __init__(self, pos, upper):
                self.pos = pos
                self.upper = upper

        # Merge sort...
        shellPts = []
        i, j = 0, 0
        while i < len(lowerShell) and j < len(upperShell):
            if lowerShell[i].x < upperShell[j].x:
                shellPts.append(ShellPt(lowerShell[i], False))
                i += 1
            else:
                shellPts.append(ShellPt(upperShell[j], True))
                j += 1

        if i < len(lowerShell):
            shellPts += map(lambda x: ShellPt(x, False), lowerShell[i:])

        if j < len(upperShell):
            shellPts += map(lambda x: ShellPt(x, True), upperShell[j:])

        # Search for largest difference
        difference = 0.0
        lastUpperPoint = None
        lastLowerPoint = None

        for i in range(len(shellPts)):

            sp = shellPts[i]
            nextUpperPoint = next((pt for pt in shellPts[i:] if pt.upper), None)
            if not nextUpperPoint:
                break

            nextLowerPoint = next((pt for pt in shellPts[i:] if not pt.upper), None)
            if not nextLowerPoint:
                break

            # Skip initial upper points
            if sp.upper and lastLowerPoint == None:
                if nextLowerPoint.pos.x == sp.pos.x:
                    difference = max(difference, sp.pos.y - nextLowerPoint.y)
                lastUpperPoint = sp
                continue
            elif not sp.upper and lastUpperPoint == None:
                if nextUpperPoint.pos.x == sp.pos.x:
                    difference = max(difference, nextUpperPoint.y - sp.pos.y)
                lastLowerPoint = sp
                continue

            ly = sp.pos.y
            uy = ly

            if not sp.upper:

                # Calculate the line going through the upper points...
                lup = lastUpperPoint.pos
                nup = nextUpperPoint.pos
                if lup.y == nup.y:
                    uy = max(lup.y, nup.y)
                else:
                    m = (nup.y - lup.y) / (nup.x - lup.x)
                    b = lup.y - m * lup.x
                    uy = m * sp.pos.x + b

            # Last lower point exists here...
            else: #sp.upper

                llp = lastLowerPoint.pos
                nlp = nextLowerPoint.pos

                if llp.y == nlp.y:
                    ly = min(llp.y, nlp.y)
                else:
                    m = (nlp.y - llp.y) / (nlp.x - llp.x)
                    b = llp.y - m * llp.x
                    ly = m * sp.pos.x + b

            d = uy - ly
            if d > difference: difference = d

        # End for loop

        # First move the player out of collision.
        self.pos += n * difference

        # Then, set the component of his velocity to be zero in this component...
        self.vel = Vector2(0,0)

    def collide(self, obj):        
        
        if isinstance(obj, Collider) and obj.collide(self):
            self.colliderResponse(obj)

    def process(self, dt): 
        self.vel += self.acc * dt	
        self.pos += self.vel * dt

        if self.collidedLastFrame:
            self.acc = Player.ACCELERATION

        self.collidedLastFrame = False

        super(Player, self).process(dt)

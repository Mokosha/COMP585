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
from colorvortex import *
from laser import Laser
from finish import FinishObject

# Simple game object that we put in our level definition files to figure out
# where to load the player in each zone...
class PlayerStartGizmo(GameObject):
    def __init__(self):
        super(PlayerStartGizmo, self).__init__()

class Player(AnimatedObject):

    MOVE_SPEED_X = 2.0
    INITIAL_JUMP = 4.0
    ACCELERATION = Vector2(0,-9.8)

    def __init__(self):

        self.currentColor = pygame.color.Color("black")
        self.changeColor(self.currentColor)

	self.colorReserves = [0, 0, 0]
	self.colorNums = []
        super(Player, self).__init__("idle", True)
        self.loadAnim("walk", True)
        self.loadAnim("fall", False)
        self.loadAnim("jump", False)

        # Initially start in the middle of the screen.
        self.pos = screen2worldPos(Vector2(0, 0), 0.5 * Vector2(screenSizeX(), screenSizeY()))
        self.vel = Vector2(0,0)
        self.acc = Player.ACCELERATION

        self.collidedLastFrame = False

        self.dynamic = True
        self.dead = False
        self.finished = False

    def changeColor(self,toChangeColor):
        self.color = self.currentColor

    def jumping(self):
        return not (self.collidedLastFrame and self.vel.y == 0.0)

    def update(self, inputManager):

        if self.dead:
            return

        if inputManager.isCurrentEvent(Events.MOVE_LEFT):
            self.vel.x = -Player.MOVE_SPEED_X
            if not self.jumping():
                self.startAnimation("walk", time.time())

        if inputManager.isCurrentEvent(Events.MOVE_RIGHT):
            self.vel.x = Player.MOVE_SPEED_X
            if not self.jumping():
                self.startAnimation("walk", time.time())

        if inputManager.isCurrentEvent(Events.JUMP):
            if not self.jumping():
                self.vel = Vector2(0, Player.INITIAL_JUMP)
#                self.startAnimation("jump", time.time())

        if inputManager.debounceEvent(Events.CHANGE_COLOR_1):
	    if self.colorReserves[0] > 0 and self.currentColor.r < 255:
            	self.currentColor.r = min(self.currentColor.r + 128, 255)
            	self.changeColor(self.currentColor)
		self.colorReserves[0] = self.colorReserves[0] - 1
	    else:
		pass

        if inputManager.debounceEvent(Events.CHANGE_COLOR_2):
	    if self.colorReserves[1] > 0 and self.currentColor.g < 255:
            	self.currentColor.g = min(self.currentColor.g + 128, 255)
            	self.changeColor(self.currentColor)
		self.colorReserves[1] = self.colorReserves[1] - 1
	    else:
		pass

        if inputManager.debounceEvent(Events.CHANGE_COLOR_3):
	    if self.colorReserves[2] > 0 and self.currentColor.b < 255:
            	self.currentColor.b = min(self.currentColor.b + 128, 255)
            	self.changeColor(self.currentColor)
		self.colorReserves[2] = self.colorReserves[2] - 1
	    else:
		pass

        if inputManager.debounceEvent(Events.RESET_COLOR):
            self.currentColor = pygame.color.Color("black")
            self.changeColor(self.currentColor)
                
        if len(inputManager.getCurrentEvents()) == 0:
            self.startAnimation("idle", time.time())
            self.vel.x = 0

    def colliderResponse(self, collider):

        # Figure out the direction at which we want to push the player out of
        # the collider. 
        n = Vector2(0, 1).rotateDeg(collider.angle)
        horiz = abs(n.dot(Vector2(0, 1))) < abs(n.dot(Vector2(1, 0)))

        direction = Vector2(0, 1 if self.vel.y <= 0 else -1)
        if horiz:
            if self.vel.x == 0:

                # !HACK! If we're not going anywhere in the x direction and
                # we're still colliding, then we need to resolve the collision
                # somehow... Just look at how separated the center of the collider
                # is versus the player. The bug here is that if the velocity is 0,
                # we shouldn't have moved into a state where we're colliding...
                objpts = collider.getPoints()
                cc = Vector2(0, 0)
                for pt in objpts:
                    cc = cc + pt
                cc = cc / float(len(objpts))
                cen = self.aabb.center()
                d = cen - cc
                direction = Vector2(1 if d[0] > 0 else -1, 0)
            else:
                direction = Vector2(1 if self.vel.x <= 0 else -1, 0)

        n = direction
        pts = self.aabb.getPoints()

        anchor = None
        for pt in pts:

            behind = any(map(lambda x: (x - pt).dot(n) < 0, [p for p in pts if not p is pt]))
            if not behind:
                anchor = pt
                break

        cpts = collider.getPoints()
        canchor = None
        for pt in cpts:
            behind = all([(x - pt).dot(n) <= 0 for x in [p for p in cpts if not p is pt]])
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

        def monotonic(shell):
            for i in range(len(shell)-1):
                if shell[i].x > shell[i+1].x:
                    return False
            return True

        lowerShell = [Vector2(v.dot(xAxis), v.dot(yAxis)) for v in lowerShell]
        if not monotonic(lowerShell):
            lowerShell = list(reversed(lowerShell))

        upperShell = [Vector2(v.dot(xAxis), v.dot(yAxis)) for v in upperShell]
        if not monotonic(upperShell):
            upperShell = list(reversed(upperShell))

        class ShellPt:
            def __init__(self, pos, upper):
                self.pos = pos
                self.upper = upper

            def __str__(self):
                return "{pos: "+str(self.pos)+", upper: "+self.upper+"}"

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
            shellPts += [ShellPt(x, False) for x in lowerShell[i:]]

        if j < len(upperShell):
            shellPts += [ShellPt(x, True) for x in upperShell[j:]]

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
                    difference = max(difference, sp.pos.y - nextLowerPoint.pos.y)
                lastUpperPoint = sp
                continue
            elif not sp.upper and lastUpperPoint == None:
                if nextUpperPoint.pos.x == sp.pos.x:
                    difference = max(difference, nextUpperPoint.pos.y - sp.pos.y)
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

                lastLowerPoint = sp

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

                lastUpperPoint = sp

            d = uy - ly
            if d > difference: difference = d

        # End for loop

        # First move the player out of collision.
        self.pos += n * (difference + 1e-5)

        # Then, set the component of his velocity to be zero in this component...
        if horiz:
            self.vel.x = 0.0
        else:
            self.vel.y = 0.0

        self.collidedLastFrame = True
        self.resetAABB()

    def collide(self, obj):

        if self.dead:
            return
        
        if isinstance(obj, Collider) and obj.collide(self):
            if obj.color != None:
                if obj.color == self.color:
                    self.colliderResponse(obj)
            else:
                self.colliderResponse(obj)
        elif isinstance(obj, ColorVortex) and obj.aabb.collideBox(self.aabb):
            #self.colorNums = []
            if obj.color.r > 0:
                if not 0 in self.colorNums: self.colorNums.append(0)
            if obj.color.g > 0: 
                if not 1 in self.colorNums: self.colorNums.append(1)
            if obj.color.b > 0:
                if not 2 in self.colorNums: self.colorNums.append(2)

        elif isinstance(obj, Laser) and obj.aabb.collideBox(self.aabb):
            if obj.color != self.color:
                self.dead = True
                self.startAnimation("fall", time.time()) 
                self.vel.x = -self.vel.x
                self.vel.y = Player.INITIAL_JUMP
        elif isinstance(obj, FinishObject) and obj.aabb.collideBox(self.aabb):
            self.finished = True

    def process(self, dt): 
        self.vel += self.acc * dt	
        self.pos += self.vel * dt

        if self.collidedLastFrame:
            self.acc = Player.ACCELERATION

        self.collidedLastFrame = False

        super(Player, self).process(dt)

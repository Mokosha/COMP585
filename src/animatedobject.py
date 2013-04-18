################################################################################
################################################################################
#
# animatedobject.py
#
# This file contains the base implementation for all of the objects that belong
# to an animation.
# 
################################################################################

import pygame, os, time, copy
import animation
from gameobject import *
from utils import *

FPS = 25
BLENDTIME = 0.2 # The amount of time it takes to blend between two animations in seconds

class AnimatedObject(GameObject):

    def __init__(self, idle_name, loop=False):
        super(AnimatedObject, self).__init__()
        self.animations = {}
        self.loadAnim(idle_name, loop)
        self.currentAnim = self.animations[idle_name]
        self.previousAnim = None
        self.previousAnimStartTime = None
        self.currentPose = copy.deepcopy(self.currentAnim.limb)
        self.animStopTime = -1
        self.animStartTime = time.time()
        self.animElapsedTime = 0.0
        self.color = None

    def loadAnim(self, name, loop):
        assets_path = getRootPath() + os.sep + "assets"

        self.animations[name] = animation.load(assets_path + os.sep + name + ".spe")
        self.animations[name].setLoop(loop)

        print "Loaded " + name + " with " + str(self.animations[name].getMaxFrame()) + " frames"

    def startAnimation(self, name, time):

        # Is the animation already started?
        if name == self.currentAnim.name:
            return

        self.previousAnimStartTime = self.animStartTime
        self.animStartTime = time
        self.animElapsedTime = 0.0
        self.animStopTime = time - 1
        self.previousAnim = self.currentAnim
        self.currentAnim = self.animations[name]

    def stopAnimation(self):
        self.animStopTime = time.clock()

    def isPlaying(self):
        return self.animStartTime > self.animStopTime

    def getCurrentFrame(self):
        # Figure out frame number
        frame = FPS * self.animElapsedTime

        if self.currentAnim.loop:
            frame = (frame % (self.currentAnim.getMaxFrame() - 1)) + 1

        return frame

    def updatePose(self):

        def updateAttr(attr, newattr, oldattr, t):

            frame = self.getCurrentFrame()
            oldframe = 0
            if self.previousAnim:
                st = self.previousAnimStartTime
                elapsed = self.animElapsedTime + (self.animStartTime - st)
                oldframe = FPS * elapsed

                if self.previousAnim.loop:
                    oldframe = (oldframe % (self.previousAnim.getMaxFrame() - 1)) + 1

            attr.animationKeys = {}
            if oldattr != None:
                oldval = oldattr.getValue(oldframe)
                newval = newattr.getValue(frame)
                attr.initialValue = smoothstep(oldval, newval, t)
            else:
                attr.initialValue = newattr.getValue(frame)

        def updateLimb(limb, newlimb, oldlimb, t):

            for attr in limb.attribs.keys():
                if oldlimb != None:
                    updateAttr(limb.attribs[attr], newlimb.attribs[attr], oldlimb.attribs[attr], t)
                else:
                    updateAttr(limb.attribs[attr], newlimb.attribs[attr], None, 0)

            assert len(limb.children) == len(newlimb.children)
            assert oldlimb == None or len(limb.children) == len(oldlimb.children)

            for idx in range(len(limb.children)):
                if oldlimb == None:
                    updateLimb(limb.children[idx], newlimb.children[idx], None, t)
                else:
                    updateLimb(limb.children[idx], newlimb.children[idx], oldlimb.children[idx], t)

        newlimb = self.currentAnim.limb
        oldlimb = None
        if self.previousAnim != None:
            oldlimb = self.previousAnim.limb

        updateLimb(self.currentPose, newlimb, oldlimb, self.animElapsedTime / BLENDTIME)

    def resetAABB(self):

        # Update AABB
        self.aabb.removeAll()

        def populateAABB(aabb, limb, frame, pos, ang, offset):

            dummyCam = Vector2(0, 0)
            aabb.add_point(pos + offset)

            sspos = world2screenPos(dummyCam, pos)
            for child in limb.children:
                newsspos, newang = child.computeNewPos(frame, sspos, ang)
                newpos = screen2worldPos(dummyCam, newsspos)
                populateAABB(aabb, child, frame, newpos, newang, offset)

        populateAABB(self.aabb, 
                     self.currentAnim.limb, 
                     self.getCurrentFrame(), 
                     Vector2(0, 0), 0, 
                     self.pos)


    def process(self, dt):

        # If the animation is stopped, then we should draw at exactly the point at which
        # it was stopped...
        self.animElapsedTime += dt
        if self.animStopTime > self.animStartTime:
            self.animElapsedTime = self.animStopTime - self.animStartTime

        if self.animElapsedTime > BLENDTIME:
            self.previousAnim = None
            self.previousAnimStartTime = None

        self.updatePose()
        self.resetAABB()

    def render(self, surface, campos):
        super(AnimatedObject, self).render(surface, campos)
        renderpos = world2screenPos(campos, self.pos)
        self.currentPose.draw(self.getCurrentFrame(), surface, renderpos, 0, self.color)

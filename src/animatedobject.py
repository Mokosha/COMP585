################################################################################
################################################################################
#
# animatedobject.py
#
# This file contains the base implementation for all of the objects that belong
# to an animation.
# 
################################################################################

import pygame, os, time
import animation
from gameobject import *
from utils import *

FPS = 25

class AnimatedObject(GameObject):

    def __init__(self, idle_name, loop=False):
        super(AnimatedObject, self).__init__()
        self.animations = {}
        self.loadAnim(idle_name, loop)
        self.currentAnim = self.animations[idle_name]
        self.animStopTime = -1
        self.animStartTime = time.time()

    def loadAnim(self, name, loop):
        assets_path = getRootPath() + os.sep + "assets"

        self.animations[name] = animation.load(assets_path + os.sep + name + ".spe")
        self.animations[name].setLoop(loop)

    def startAnimation(self, name, time):
        self.animStartTime = time
        self.animStopTime = time - 1
        self.currentAnim = self.animations[name]

    def stopAnimation(self):
        self.animStopTime = time.clock()

    def isPlaying(self):
        return self.animStartTime > self.animStopTime

    def render(self, time, surface, campos):
        
        # If the animation is stopped, then we should draw at exactly the point at which
        # it was stopped...
        if self.animStopTime > self.animStartTime:
            time = self.animStopTime

        # Figure out frame number
        elapsed = time - self.animStartTime
        frame = FPS * elapsed

        if self.currentAnim.loop:
            frame = (frame % (self.currentAnim.getMaxFrame() - 1)) + 1

        renderpos = world2screenPos(campos, self.pos)
        self.currentAnim.draw(frame, surface, renderpos)
        

################################################################################
################################################################################
#
# animatedobject.py
#
# This file contains the base implementation for all of the objects that belong
# to an animation.
# 
################################################################################

import pygame, os
import animation
from gameobject import *

FPS = 25

class AnimatedObject(GameObject):

	def __init__(self, idle_name, loop=False):
		self.animations = {}
		self.loadAnim(idle_name, loop)
		self.currentAnim = self.animations[idle_name]

	def loadAnim(self, name, loop):
		assets_path = os.path.realpath(__file__).split(os.sep)[:-2]
		assets_path = os.sep.join(assets_path) + os.sep + "assets"

		self.animations[name] = animation.load(assets_path + os.sep + name + ".spe")
		self.animations[name].setLoop(loop)

	def startAnimation(self, name, time):
		self.animStartTime = time
		self.currentAnim = self.animations[name]

	def draw(self, time, surface, pos):
		
		# Figure out frame number
		elapsed = time - self.animStartTime
		frame = FPS * elapsed

		if self.currentAnim.loop:
			frame = (frame % self.currentAnim.getMaxFrame()) + 1

		self.currentAnim.draw(frame, surface, pos)
		

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

	def __init__(self, idle_name):
		self.animations = {}
		self.loadAnim(idle_name)
		self.currentAnim = self.animations[idle_name]

	def loadAnim(self, name):
		assets_path = os.path.realpath(__file__).split(os.sep)[:-2]
		assets_path = os.sep.join(assets_path) + os.sep + "assets"

		self.animations[name] = animation.load(assets_path + os.sep + name + ".spe")

	def startAnimation(self, name, time):
		self.animStartTime = time
		self.currentAnim = self.animations[name]

	def draw(self, time, surface, pos):
		
		# Figure out frame number
		elapsed = time - self.animStartTime
		frame = FPS * elapsed
		self.currentAnim.draw(frame, surface, pos)
		

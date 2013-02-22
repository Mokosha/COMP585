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

class AnimatedObject(GameObject):

	def __init__(self, idle_name):
		self.animations = {}
		self.loadAnim(idle_name)
		self.currentAnim = self.animations[idle_name]

	def loadAnim(self, name):
		assets_path = os.path.realpath(__file__).split('/')[:-2]
		assets_path = "/".join(assets_path) + "/assets"

		self.animations[name] = animation.load(assets_path + "/" + name + ".spe")

	def setAnimation(self, name):
		pass

################################################################################
################################################################################
#
# gameobject.py
#
# This file contains the base implementation for all of the game objects in the
# game. Game objects are objects that conform to a certain set of rules:
# 
# 1. They have a position and orientation
# 2. They can be drawn
# 3. They can respond to input events
#
################################################################################

import pygame

class GameObject:

	def __init__(self):
		self.pos = (0, 0)
		self.angle = 0


	def render(self):
		pass

	def accept(event):
		pass

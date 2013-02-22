################################################################################
################################################################################
#
# animation.py
#
# This file contains the definitions and structure of a 2D keyframed animation
# 
################################################################################

import pygame
import xml.etree.ElementTree as ET

class Animation:

	def __init__(self, filename):
		self.loadFile(filename)

	def loadFile(self, filename):
		tree = ET.parse(filename)
		root = tree.getroot()
		print root.tag
		print root.attrib

def load(filename):
	return Animation(filename)

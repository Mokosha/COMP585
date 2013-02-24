################################################################################
################################################################################
#
# animation.py
#
# This file contains the definitions and structure of a 2D keyframed animation
# 
################################################################################

import math, re
import pygame
import xml.etree.ElementTree as ET
from lib.euclid import *
from utils import *

class AnimationAttribute:

	def __init__(self, node):
		self.keys = {}
		self.loadAttribute(node)

	def loadValue(self, value):

		fltRegEx = re.compile("[+-]? *(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?")

		if value == "True":
			return True

		elif value == "False":
			return False

		elif value[0] == "[":
			floatList = [float(x) for x in fltRegEx.findall(value)]
			if len(floatList) == 2:
				return Vector2(floatList[0], floatList[1])
			elif len(floatList) == 3:
				return Vector3(floatList[0], floatList[1], floatList[2])
			else:
				assert not "Unknown list type!"

		elif fltRegEx.match(value):
			return float(value)

		else:
			return value

	def loadAttribute(self, node):
		self.name = node.tag

		keyframes = node.findall("keyframe")
		assert len(keyframes) == 1

		keyframe = keyframes[0]

		self.initialValue = self.loadValue(keyframe.get("value"))
		assert self.initialValue != None

		self.interpolationType = keyframe.get("interpol")
		assert self.interpolationType != None

		self.animationKeys = {int(key.get("frame")):self.loadValue(key.get("value")) for key in keyframe}

	def getValue(self, frame):
		prevKey = None
		nextKey = None
		for keyframe in self.animationKeys.keys():
			if keyframe < frame:
				if prevKey == None or keyframe > prevKey:
					prevKey = keyframe
			elif keyframe > frame:
				if nextKey == None or keyframe < nextKey:
					nextKey = keyframe

		if prevKey == None:
			return self.initialValue

		if nextKey == None:
			return self.animationKeys[nextKey]

		if self.interpolationType == "const":
			return self.animationKeys[prevKey]
		elif self.interpolationType == "linear":
			keyDist = nextKey - prevKey
			pct = ((frame - prevKey) * 1.0) / keyDist
			return lerp(self.animationKeys[prevKey], self.animationKeys[nextKey], pct)
		else:
			assert not "Unknown interpolation method!"

class Shape:
	
	def __init__(self, node):
		self.attribs = {}
		
		textures = node.findall("texture")
		assert len(textures) == 1

		texture = textures[0]
		for child in texture:
			self.attribs[child.tag] = AnimationAttribute(child)
	
	def draw(self, frame, surface, pt1, pt2, color, width):

		if self.attribs['shape'].getValue() == "line":
			x1, y1 = int(pt1.x), int(pt1.y)
			x2, y2 = int(pt2.x), int(pt2.y)

			pygame.draw.line(surface, color, (x1, y1), (x2, y2), width)

		elif self.attribs['shape'].getValue() == "circle":
			c = (pt1 + pt2)*0.5
			r = (pt2-pt1).magnitude * 0.5
			
			cx, cy = int(c.x), int(c.y)
			
			pygame.draw.circle(surface, color, (cx, cy), r, width)
		elif self.attribs['shape'].getValue() == "text":
			pass
		elif self.attribs['shape'].getValue() == "image":
			pass
		else:
			pass

class Limb:
	
	def __init__(self, node):
		self.attribs = {}
		for child in node:
			if child.tag == "children":
				self.children = [Limb(x) for x in child]
			elif child.tag == "shape":
				self.shape = Shape(child)
			else:
				self.attribs[child.tag] = AnimationAttribute(child)

	def draw(self, frame, surface, pos, ang):
	
		color = self.attribs['colour'].getValue(frame)

		if self.attribs['cartesian']:
			newAng = ang
			newPos = pos + self.attribs['pos'].getValue(frame)

		else:
			newAng = ang + self.attribs['ang'].getValue(frame)
			dist = self.attribs['dist'].getValue(frame)
			
			newPos = pos + polar2cart(newAng, dist)

		if not self.attribs['hidden']:
			width = self.attribs['width'].getValue(frame)
			self.attribs['shape'].draw(frame, surface, pos, newPos, color, width)

		for limb in self.children:
			limb.draw(frame, surface, newPos, newAng)
	
class Animation:

	def __init__(self, filename):
		self.loadFile(filename)

	def loadFile(self, filename):
		tree = ET.parse(filename)
		root = tree.getroot()
		assert root.tag == "limb"
		self.limb = Limb(root)

	def draw(self, frame, surface, pos):
		self.limb.draw(frame, surface, pos)

def load(filename):
	return Animation(filename)

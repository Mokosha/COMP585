import sys, time
from utils import *

import pygame

from eventmanager import Events, InputManager

class Screen:

	myOptions = []

	def __init__(self, topLeftCorner, width, height, layout, bckgrdClr):
		self.loc = topLeftCorner
		self.mySurface = pygame.Surface((width, height))
		self.layout = layout
		self.color = bckgrdClr
		self.mySurface.fill(self.color)

	def runMenu(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				elif event.type == 

class Options:

	def __init__(self, parent, topLeftRelative, width, height, text):
		font = pygame.font.SysFont('comicsansms',32)
		self.newSurface = font.render(text, True, pygame.Color('white'))
		if (parent.layout == 'horiz'):
			pass
		elif (parent.layout == 'vert'):
			xOffset = self.findCentralPosition(parent.mySurface.get_width(),width)
			yOffset = topLeftRelative * (height + 50)
			print(((parent.loc[0] + xOffset), (parent.loc[1] + yOffset)))
			print((parent.loc[0], parent.loc[1], parent.mySurface.get_width(), parent.mySurface.get_height()))
			parent.mySurface.blit(self.newSurface, (xOffset, yOffset))
		parent.myOptions.append(self)

	def findCentralPosition(self, outerLength, innerLength):
		return ((outerLength - innerLength) / 2)
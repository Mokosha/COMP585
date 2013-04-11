import sys, time
from utils import *

import pygame

def initMenu(theSurface):
	myMenu = Screen((150, 100), 300, 400, 'vert', pygame.Color('orange'))
	optionsone = Options(myMenu, 0, 200, 50, 'Resume')
	optionstwo = Options(myMenu, 1, 200, 50, 'Help')
	optionsthree = Options(myMenu, 2, 200, 50, 'Return to Title')
	theSurface.blit(myMenu.mySurface, myMenu.loc)

class Screen:

	def __init__(self, topLeftCorner, width, height, layout, bckgrdClr):
		self.loc = topLeftCorner
		self.mySurface = pygame.Surface((width, height))
		self.layout = layout
		self.color = bckgrdClr
		self.mySurface.fill(self.color)


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

	def findCentralPosition(self, outerLength, innerLength):
		return ((outerLength - innerLength) / 2)
import os, sys, time
from utils import *

import pygame

from eventmanager import Events, InputManager

def makeFinishGameScreen(surface, levelName):
	mytext = "Completed the game!"
	options = ["Play again", "Return to Title"]
	return NextLevelScreen(surface, mytext, options, getAssetsPath() + os.sep + "rainbow.png").runMenu()

def makeNextLevelScreen(surface, levelName):
	mytext = "Completed the level " + levelName
	options = ["Next Level", "Return to Title"]
	if levelName == "start":
		imagename = "emptyhalfrainbow"
	if levelName == "next":
		imagename = "rainbow"
	return NextLevelScreen(surface, mytext, options, getAssetsPath() + os.sep + imagename + ".png").runMenu()

class DialogBox(object):

	def __init__(self, drawSurface, text, options, image):
		self.drawSurface = drawSurface
		self.currentlySelected = 0
		self.text = text
		self.options = options
		self.image = pygame.image.load(image)
		self.drawSurface.fill(pygame.Color('white'))
		self.drawMenu()

	def drawMenu(self):
		self.drawSurface.fill(pygame.Color('white'))
		self.drawSurface.blit(pygame.font.SysFont("comicsansms", 32).render(self.text, False, pygame.Color('black')), (250, 60))
		self.drawSurface.blit(self.image, (50, 130))
		for i in range(len(self.options)):
			textsize = 24
			if self.currentlySelected == i:
				textsize = 28
			self.drawSurface.blit(pygame.font.SysFont("comicsansms", textsize).render(self.options[i], False, pygame.Color('black')), (250, 450 + (i * 40)))

		pygame.display.flip()
		
	def runMenu(self):
		pygame.event.clear()
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
					if self.currentlySelected == 0:
						self.currentlySelected = len(self.options) - 1
					else:
						self.currentlySelected = self.currentlySelected - 1
					self.drawMenu()
				if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
					if self.currentlySelected == len(self.options) - 1:
						self.currentlySelected = 0
					else:
						self.currentlySelected = self.currentlySelected + 1
					self.drawMenu()
				if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
					return self.execute()
				if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
					self.currentlySelected = 0
					return self.execute()

	def execute(self):
		return ""

class NextLevelScreen(DialogBox):

	def execute(self):
		if self.currentlySelected == 0:
			return "Next"
		else:
			return "Back"


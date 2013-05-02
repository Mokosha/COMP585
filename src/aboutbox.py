import os, sys, time
from utils import *

import pygame

from eventmanager import Events, InputManager

class AboutBox:

	def __init__(self, drawSurface, text):
		self.text = text
		self.drawSurface = drawSurface
		self.drawSurface.fill(pygame.Color("orange"))
		font = pygame.font.SysFont('comicsansms', 24)
		lines = text.splitlines()
		for i in range(len(lines)):
			textSurface = font.render(lines[i], True, pygame.Color('black'))
			self.drawSurface.blit(textSurface, (50, 50 + (i * 50)))
		pygame.display.flip()

	def runAboutMenu(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				elif event.type == pygame.KEYDOWN:
					return "Update"
			
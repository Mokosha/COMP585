################################################################################
################################################################################
#
# main.py
#
# This file contains the game loop for the game. It serves as a controller for
# hooking all of the pieces (rendering, input, updates) together
#
################################################################################

import sys

import pygame
pygame.init()

import animatedobject

WINDOW_SIZE_X=800
WINDOW_SIZE_Y=600
pygame.display.set_mode((WINDOW_SIZE_X, WINDOW_SIZE_Y))

obj = animatedobject.AnimatedObject("wave")

while True:
	pygame.display.update()
	for event in pygame.event.get():
		if event.type in (pygame.QUIT, pygame.KEYDOWN):
			sys.exit()
	

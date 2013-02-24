################################################################################
################################################################################
#
# main.py
#
# This file contains the game loop for the game. It serves as a controller for
# hooking all of the pieces (rendering, input, updates) together
#
################################################################################

import sys, time

import pygame
pygame.init()

import animatedobject

WINDOW_SIZE_X=800
WINDOW_SIZE_Y=600

START_TIME = time.clock()

pygame.display.set_mode((WINDOW_SIZE_X, WINDOW_SIZE_Y))

display_surface = pygame.display.get_surface()
display_surface.fill((255, 255, 255))

obj = animatedobject.AnimatedObject("wave", True)
obj.startAnimation("wave", START_TIME)

while True:

	cur_time = time.clock()
	
	display_surface.fill((255, 255, 255))
	obj.draw(cur_time, display_surface, (WINDOW_SIZE_X/2, WINDOW_SIZE_Y/2))

	for event in pygame.event.get():
		if event.type in (pygame.QUIT, pygame.KEYDOWN):
			sys.exit()

	pygame.display.update()
	

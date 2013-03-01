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
video_info = pygame.display.Info()
window_w, window_h = video_info.current_w, video_info.current_h

import animatedobject

WINDOW_SIZE_X=800
WINDOW_SIZE_Y=600

START_TIME = time.clock()

pygame.display.set_mode((WINDOW_SIZE_X, WINDOW_SIZE_Y))
fullscreen = pygame.display.toggle_fullscreen()

display_surface = pygame.display.get_surface()
display_surface.fill((255, 255, 255))

obj = animatedobject.AnimatedObject("smooth-idle", True)
obj.startAnimation("smooth-idle", START_TIME)

while True:

    cur_time = time.clock()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                if obj.isPlaying():
                    obj.stopAnimation()
                else:
                    obj.startAnimation("smooth-idle", START_TIME)
            else:
                if fullscreen:
                    pygame.display.set_mode((window_w, window_h))
                    pygame.display.toggle_fullscreen()
                sys.exit()

    display_surface.fill((255, 255, 255))
    obj.draw(cur_time, display_surface, (WINDOW_SIZE_X/2, WINDOW_SIZE_Y/2))

    pygame.display.update()
    

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
from utils import *

import pygame
pygame.init()
pygame.display.set_mode((screenSizeX(), screenSizeY()))

import animatedobject, colorvortex
from lib.euclid import *

video_info = pygame.display.Info()
window_w, window_h = video_info.current_w, video_info.current_h

START_TIME = time.clock()

#fullscreen = pygame.display.toggle_fullscreen()
fullscreen = False

display_surface = pygame.display.get_surface()
display_surface.fill((255, 255, 255))

camera_pos = Vector2(0, 0)

player = animatedobject.AnimatedObject("smooth-idle", True)
player.startAnimation("smooth-idle", START_TIME)

# Move it to the center of the screen just for funsies...
player.pos = screen2worldPos(camera_pos, 0.5 * Vector2(screenSizeX(), screenSizeY()))

cv = colorvortex.ColorVortex(Vector2(1, 1))

game_objects = [player, cv]
x = screenSizeX()
paused = False

while True:

    cur_time = time.clock()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                x += 10
                player.pos = screen2worldPos(camera_pos, 0.5 * Vector2(x, screenSizeY()))
            elif event.key == pygame.K_LEFT:
                x -= 10
                player.pos = screen2worldPos(camera_pos, 0.5 * Vector2(x, screenSizeY()))
            elif event.key == pygame.K_s:
                if obj.isPlaying():
                    obj.stopAnimation()
                else:
                    obj.startAnimation("smooth-idle", START_TIME)
            elif event.key == pygame.K_SPACE:
                paused = not paused
            else:
                if fullscreen:
                    pygame.display.set_mode((window_w, window_h))
                    pygame.display.toggle_fullscreen()
                sys.exit()

    if paused:
        continue

    display_surface.fill((255, 255, 255))
    for obj in game_objects:
        obj.render(cur_time, display_surface, camera_pos)

    pygame.display.update()
    

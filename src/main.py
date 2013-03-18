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
from eventmanager import Events, InputManager
from lib.euclid import *

# Initialize Display
video_info = pygame.display.Info()
window_w, window_h = video_info.current_w, video_info.current_h

START_TIME = time.clock()

#fullscreen = pygame.display.toggle_fullscreen()
fullscreen = False

display_surface = pygame.display.get_surface()
display_surface.fill((255, 255, 255))

# Define current camera
camera_pos = Vector2(0, 0)

# Initialize Player...
player = animatedobject.AnimatedObject("smooth-idle", True)
player.startAnimation("smooth-idle", START_TIME)
player.pos = screen2worldPos(camera_pos, 0.5 * Vector2(screenSizeX(), screenSizeY()))

# !FIXME!
cv = colorvortex.ColorVortex(Vector2(1, 1))

game_objects = [player, cv]
paused = False

# Initialize input handler
inputhandler = InputManager()

while True:

    cur_time = time.clock()
    
    inputhandler.handleEvents()

    for event in inputhandler.getCurrentEvents():
        if event == Events.QUIT:
            pygame.display.set_mode((window_w, window_h))
            pygame.display.toggle_fullscreen()
            sys.exit()
        elif event == Events.PAUSE:
            paused = not paused

    if paused:
        continue

    display_surface.fill((255, 255, 255))
    for obj in game_objects:
        obj.render(cur_time, display_surface, camera_pos)

    pygame.display.update()
    

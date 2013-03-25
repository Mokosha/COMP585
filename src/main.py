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

import animatedobject, colorvortex, player, world
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
player = player.Player()

# !FIXME!
cv = colorvortex.ColorVortex(Vector2(1, 1))

game_objects = [player, cv]
paused = False

# Initialize input handler
inputhandler = InputManager()

world = world.World("start")

def handleAdministrivia(inputManager):

    if inputManager.isCurrentEvent(Events.QUIT):
        pygame.display.set_mode((window_w, window_h))
        pygame.display.toggle_fullscreen()
        sys.exit()
    elif inputManager.isCurrentEvent(Events.PAUSE):
        global paused
        paused = not paused

def render():
    display_surface.fill((255, 255, 255))

    world.render(cur_time, display_surface, camera_pos)

    for obj in game_objects:
        obj.render(cur_time, display_surface, camera_pos)

    pygame.display.update()
    

while True:

    cur_time = time.time()
    
    inputhandler.handleEvents()
    
    handleAdministrivia(inputhandler)
    
    if paused:
        continue

    camera_pos.x += 0.001

    player.update(inputhandler)

    render()

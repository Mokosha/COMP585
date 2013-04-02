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
display_info = pygame.display.Info()

print "Display is hardware accelerated: " + str(display_info.hw)
print "Windowed display modes can be used: " + str(display_info.wm)
print "Megabytes of video memory: " + str(display_info.video_mem)
print "Number of bits used to store each pixel: " + str(display_info.bitsize)
print "Number of bytes used to store each pixel: " + str(display_info.bytesize)
print "Four values used to pack RGBA values into pixels: " + str(display_info.masks)
print "Four values used to pack RGBA values into pixels: " + str(display_info.shifts)
print "Four values used to pack RGBA values into pixels: " + str(display_info.losses)
print "Hardware surface blitting is accelerated: " + str(display_info.blit_hw)
print "Hardware surface colorkey blitting is accelerated: " + str(display_info.blit_hw_CC)
print "Hardware surface pixel alpha blitting is accelerated: " + str(display_info.blit_hw_A)
print "Software surface blitting is accelerated: " + str(display_info.blit_sw)
print "Software surface colorkey blitting is accelerated: " + str(display_info.blit_sw_CC)
print "Software surface pixel alpha blitting is accelerated: " + str(display_info.blit_sw_A)

window_w, window_h = display_info.current_w, display_info.current_h

START_TIME = time.clock()

#fullscreen = pygame.display.toggle_fullscreen()
fullscreen = False

display_surface = pygame.display.get_surface()

# Define current camera
camera_pos = Vector2(0, 0)

# Initialize Player...
p = player.Player()
game_objects = [p]
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

    p.update(inputhandler)
    p.gravity()
    p.jump()

    render()

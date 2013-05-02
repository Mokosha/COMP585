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

import animatedobject, colorvortex, player, world, dialogmenu
from menumanager import PauseMenu, TitleMenu
from eventmanager import Events, InputManager
from lib.euclid import *

def handleAdministrivia(inputManager, display_surface):

    if inputManager.isCurrentEvent(Events.QUIT):
        pygame.display.set_mode((window_w, window_h))
        pygame.display.toggle_fullscreen()
        sys.exit()
    elif inputManager.isCurrentEvent(Events.PAUSE):
        message = PauseMenu().run(display_surface)
        pygame.display.flip()
        inputManager.removeCurrentEvent(Events.PAUSE)
        return message

def render(wld, campos, surface):
    surface.fill((255, 255, 255))
    wld.render(surface, camera_pos)

def processCamera(wld, dt):

    global camera_pos

    p = wld.getPlayer()

    windowSzX = screen2world(window_w)
    windowSzY = screen2world(window_h)
    
    cammin = Vector2(camera_pos.x + CAMERA_BOUNDARY_SIZE, camera_pos.y + CAMERA_BOUNDARY_SIZE)
    cammax = Vector2(camera_pos.x + windowSzX - CAMERA_BOUNDARY_SIZE, camera_pos.y + windowSzY - CAMERA_BOUNDARY_SIZE)

    desiredmin = Vector2(camera_pos.x + windowSzX * CAMERA_DRAG_PCT_X, camera_pos.y + windowSzY * CAMERA_DRAG_PCT_Y)
    desiredmax = desiredmin

    if p.pos.x > desiredmax.x:
        dist = p.pos.x - desiredmax.x
        if dist < 0.001:
            camera_pos.x += dist
        else:
            camera_pos.x += dt * CAMERA_DRAG_SPEED * dist
    elif p.pos.x < desiredmin.x:
        dist = desiredmin.x - p.pos.x
        if dist < 0.001:
            camera_pos.x -= dist
        else:
            camera_pos.x -= dt * CAMERA_DRAG_SPEED * dist

    if p.pos.y > desiredmax.y:
        dist = p.pos.y - desiredmax.y
        if dist < 0.001:
            camera_pos.y += dist
        else:
            camera_pos.y += dt * CAMERA_DRAG_SPEED * dist
    elif p.pos.y < desiredmin.y:
        dist = desiredmin.y - p.pos.y
        if dist < 0.001:
            camera_pos.y -= dist
        else:
            camera_pos.y -= dt * CAMERA_DRAG_SPEED * dist

    if p.pos.x > cammax.x:
        camera_pos.x = p.pos.x + CAMERA_BOUNDARY_SIZE - windowSzX
    elif p.pos.x < cammin.x:
        camera_pos.x = p.pos.x - CAMERA_BOUNDARY_SIZE

    if p.pos.y > cammax.y:
        camera_pos.y = p.pos.y + CAMERA_BOUNDARY_SIZE - windowSzY
    elif p.pos.y < cammin.y:
        camera_pos.y = p.pos.y - CAMERA_BOUNDARY_SIZE

    # Bound camera...
    if camera_pos.y < 0:
        camera_pos.y = 0

    cam_limit_x = float(len(wld.zones)) * world.Zone.ZONE_SIZE_X - screen2world(screenSizeX())
    camera_pos.x = clamp(camera_pos.x, 0, cam_limit_x)

def process(wld, camera_pos, dt):
    retval = wld.process(camera_pos, dt)
    processCamera(wld, dt)
    return retval

# Define current camera
camera_pos = Vector2(0, 0)
CAMERA_BOUNDARY_SIZE = 2.0
CAMERA_DRAG_CENTER = True
CAMERA_DRAG_PCT_X = 0.3
CAMERA_DRAG_PCT_Y = 0.4
CAMERA_DRAG_SPEED = 8.0

def resetCamera():
    global camera_pos
    camera_pos = Vector2(0, 0)

def runTitleMenu(mysurface):
    pygame.mixer.init()
    mysound = pygame.mixer.Sound(getAssetsPath() + os.sep + "sound" + os.sep + "Music" + os.sep + "TitleScreen.ogg")
    mysound.play(loops=-1)
    result = TitleMenu().run(mysurface)
    pygame.mixer.stop()
    return result

def setLevelSound(levelName):
    pygame.mixer.init()
    global mysound
    mysound = pygame.mixer.Sound(getAssetsPath() + os.sep + "sound" + os.sep + "Music" + os.sep + levelName + ".ogg")
    mysound.play(loops=-1, fade_ms=2000)

def stopSound():
    pygame.mixer.stop()

# Initialize input handler
inputhandler = InputManager()

# Main Loop
while True:

    window_w, window_h = display_info.current_w, display_info.current_h
    display_surface = pygame.display.get_surface()
    mylevel = "start"
    option = runTitleMenu(display_surface)
    if option != None:
	mylevel = option
    resetCamera()
    w = world.World(mylevel) if len(sys.argv) == 1 else world.World(mylevel, int(sys.argv[1]))
    setLevelSound(mylevel)

    last_time = time.time()

    # Game loop
    while True:

        cur_time = time.time()
        dt = cur_time - last_time
        if dt <= 0:
            time.sleep(0.001)
            last_time = cur_time
            continue

        inputhandler.handleEvents()

        message = handleAdministrivia(inputhandler, display_surface)
        if message == "Quit Game":
            break

        if message != None:
            last_time = time.time()
            continue

        w.getPlayer().update(inputhandler)

        if process(w, camera_pos, dt) == "FINISH":
            inputhandler.clearEvents()
            if w.levelname == "start":
                stopSound()
                if dialogmenu.makeNextLevelScreen(display_surface, w.levelname) == "Back":
                    break
                w = world.World("next")
                setLevelSound("next")
            else:
		stopSound()
                if dialogmenu.makeFinishGameScreen(display_surface, w.levelname) == "Back":
                    break
                w = world.World("start")
                setLevelSound("start")

            last_time = time.time()
        else:
            render(w, camera_pos, display_surface)
            pygame.display.update()

            last_time = cur_time

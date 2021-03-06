################################################################################
################################################################################
#
# colorvortex.py
#
# This file contains the base implementation for all of the game objects in the
# game. Game objects are objects that conform to a certain set of rules:
# 
# 1. They have a position and orientation
# 2. They can be drawn
# 3. They can respond to input events
#
################################################################################

import pygame, time, copy

from particlesystem import *
from gameobject import *
from lib.euclid import *
from utils import *

COLOR_VORTEX_SCREEN_SIZE = 64
COLOR_VORTEX_WORLD_SIZE = screen2world(COLOR_VORTEX_SCREEN_SIZE)

# We have 8 frames but only two sprites... we do this because we can achieve more 
# variation if we rotate the image by 90 degrees every two frames...
VORTEX_FRAMES = 8
VORTEX_SPRITES = 2

# This is the speed at which the vortices spin... This is measured in time between frames.
VORTEX_SPIN_SPEED = 0.07

class ColorVortex(GameObject):
    spritesheet = pygame.image.load(getRootPath() + os.sep + "assets" + os.sep + "colorvortex.png")
    spritesheet = pygame.transform.smoothscale(spritesheet.convert_alpha(), (2 * COLOR_VORTEX_SCREEN_SIZE, COLOR_VORTEX_SCREEN_SIZE))

    def setpos(self, newpos):
        super(ColorVortex, self).setpos(newpos)
        for emitter in filter(lambda x: x.emitter, self.ps.actions):
            emitter.addPosDomain(CircleDomain(newpos, 0.1))

        self.aabb.removeAll()
        halfVortexSize = 0.5 * Vector2(COLOR_VORTEX_WORLD_SIZE,COLOR_VORTEX_WORLD_SIZE)
        self.aabb.add_point(newpos - halfVortexSize)
        self.aabb.add_point(newpos + halfVortexSize)
        

    def __init__(self, pos, color=pygame.Color("blue")):
        super(ColorVortex, self).__init__()
        self.pos = pos

        self.aabb.removeAll()
        halfVortexSize = 0.5 * Vector2(COLOR_VORTEX_WORLD_SIZE,COLOR_VORTEX_WORLD_SIZE)
        self.aabb.add_point(pos - halfVortexSize)
        self.aabb.add_point(pos + halfVortexSize)

        self.frame = 0
        self.elapsed = 0.0

        self.ps = ParticleSystem(20)
        emitter = EmitAction(5.0)
        emitter.addPosDomain(CircleDomain(self.pos, 0.07))
        emitter.addVelDomain(CircleDomain(Vector2(0.0, 1.5), 0.7))
        emitter.addColorDomain(PointDomain(Vector3(color.r, color.g, color.b)))

        self.ps.addAction(emitter)
        self.ps.addAction(ForceAction(Vector2(0.0, -3.0)))
        self.ps.addAction(SpinAction(230.0))
        self.ps.addAction(MoveAction())
        self.ps.addAction(FadeAction(170.0))
        self.ps.addAction(KillFadedAction())

        # Go through the spritesheet for this and change every white color
        # to the one that we passed in...
        self.spritesheet = ColorVortex.spritesheet.copy()
        self.spritesheet.lock()
        for x in range(COLOR_VORTEX_SCREEN_SIZE * 2):
            for y in range(COLOR_VORTEX_SCREEN_SIZE):
                c = self.spritesheet.get_at((x, y))
                thresh = 15
                cr, cg, cb, ca = c.normalize()
                newColor = pygame.Color(
                    int(cr * color.r), 
                    int(cg * color.g), 
                    int(cb * color.b), 
                    int(ca * 255))
                self.spritesheet.set_at((x, y), newColor)
        self.spritesheet.unlock()

        self.color = color

    def process(self, dt):
        self.elapsed += dt
        if self.elapsed > VORTEX_SPIN_SPEED:
            self.frame = (self.frame + 1) % VORTEX_FRAMES
            self.elapsed = 0.0

        self.ps.process(dt)

    def render(self, surface, campos):
        super(ColorVortex, self).render(surface, campos)

        self.ps.render(surface, campos)
        
        rot = int(self.frame / 2)
        side = self.frame % 2

        if rot >= 2:
            side = 1 - side

        surf = pygame.transform.rotate(self.spritesheet, -90 * rot)
        maskRect = pygame.Rect(
            side * ((rot + 1) % 2) * COLOR_VORTEX_SCREEN_SIZE, 
            side * (rot % 2) * COLOR_VORTEX_SCREEN_SIZE, 
            COLOR_VORTEX_SCREEN_SIZE, 
            COLOR_VORTEX_SCREEN_SIZE)

        renderPos = world2screenPos(campos, self.pos)
        renderPos.x -= 0.5 * COLOR_VORTEX_SCREEN_SIZE
        renderPos.y -= 0.5 * COLOR_VORTEX_SCREEN_SIZE

        renderRect = pygame.Rect(renderPos, (COLOR_VORTEX_SCREEN_SIZE, COLOR_VORTEX_SCREEN_SIZE))
        surface.blit(surf, renderRect, maskRect)

    def accept(self, event):
        pass

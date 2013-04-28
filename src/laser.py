################################################################################
################################################################################
#
# laser.py
#
# Game object that defines a barrier of a certain color. Once that barrier is
# hit, if the player is that color, then they pass through unharmed. Otherwise,
# the player dies.
#
################################################################################

import pygame, sys

from lib.euclid import *
from utils import *
from gameobject import *
from math import *

def scalesurf(surf):
    SCALE = 0.3
    w, h = surf.get_width(), surf.get_height()
    return pygame.transform.scale(surf, (int(w * SCALE), int(h * SCALE)))

class Laser(GameObject):

    LASER_HILT = scalesurf(pygame.image.load(getAssetsPath() + os.sep + "laserHilt.png"))
    LASER_SECTION = scalesurf(pygame.image.load(getAssetsPath() + os.sep + "laserSection.png"))
    LASER_TOP = scalesurf(pygame.image.load(getAssetsPath() + os.sep + "laserTop.png"))

    assert LASER_HILT.get_width() == LASER_SECTION.get_width()
    assert LASER_HILT.get_width() == LASER_TOP.get_width()

    def __init__(self, pos, length, color, angle = 0):
        super(Laser, self).__init__()

        self.pos = pos
        self.color = color
        self.angle = angle

        screenlen = world2screen(length) - Laser.LASER_TOP.get_height()
        if screenlen < 0:
            print "WARNING: Laser length shorter than top sprite!"

        numsections = max(0, int(math.ceil(screenlen / Laser.LASER_SECTION.get_height())))

        self.spritewidth = int(Laser.LASER_TOP.get_width())
        self.spriteheight = Laser.LASER_TOP.get_height()
        self.spriteheight += Laser.LASER_HILT.get_height()
        self.spriteheight += numsections * Laser.LASER_SECTION.get_height()
        srsize = (self.spritewidth, self.spriteheight)
        srrect = pygame.Rect((0, 0), srsize)
        self.sprite = pygame.Surface(srsize, pygame.SRCALPHA)

        dest = pygame.Rect((0, 0), (self.spritewidth, Laser.LASER_TOP.get_height()))
        self.sprite.blit(Laser.LASER_TOP, dest)

        dest.height = Laser.LASER_SECTION.get_height()
        dest.top += Laser.LASER_TOP.get_height()

        for i in range(numsections):
            self.sprite.blit(Laser.LASER_SECTION, dest)
            dest.top += Laser.LASER_SECTION.get_height()

        masksurf = pygame.Surface(srsize, pygame.SRCALPHA)
        pygame.draw.rect(masksurf, 
                         self.color, 
                         pygame.Rect((0, 0), 
                                     (self.spritewidth, self.spriteheight - Laser.LASER_HILT.get_height())))
        self.sprite.blit(masksurf, srrect, None, pygame.BLEND_RGBA_MULT)
        self.sprite.blit(Laser.LASER_HILT, dest)

        self.aabb.removeAll()
        
        pt = self.pos + screen2world(Vector2(-self.spritewidth*0.5, self.spriteheight))
        pt.y -= screen2world(Laser.LASER_HILT.get_height() * 0.5)
        self.aabb.add_point(pt)

        pt.x += screen2world(self.spritewidth)
        pt.y -= screen2world(self.spriteheight - Laser.LASER_HILT.get_height())
        self.aabb.add_point(pt)

    def render(self, surface, campos):

        worldoffset = screen2world(Vector2(-self.spritewidth * 0.5, self.spriteheight))
        worldoffset.y -= screen2world(Laser.LASER_HILT.get_height()) * 0.5
        tl = world2screenPos(campos, self.pos + worldoffset)

        surface.blit(self.sprite, pygame.Rect(tl, (self.spritewidth, self.spriteheight)))
        super(Laser, self).render(surface, campos)

    def accept(self, event):
        pass

    def process(self, dt):
        pass

    def collide(self, obj):
        return False


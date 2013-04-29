################################################################################
################################################################################
#
# finish.py
#
# This game object reflects the end of a level. Level end markers are denoted
# by pieces of rainbow with particle effects. Once the player runs into this
# game object, the world knows to load the next level...
#
################################################################################

import pygame, time, copy

from particlesystem import *
from gameobject import *
from lib.euclid import *
from utils import *

FINISH_WORLD_SIZE = 1.0
FINISH_SCREEN_SIZE = int(world2screen(FINISH_WORLD_SIZE))

class FinishObject(GameObject):
    sprite = pygame.transform.scale(pygame.image.load(getAssetsPath() + os.sep + "halfrainbow.png"),
                                    (FINISH_SCREEN_SIZE, FINISH_SCREEN_SIZE))

    def resetaabb(self):
        self.aabb.removeAll()
        halfFinishSize = 0.5 * Vector2(FINISH_WORLD_SIZE, FINISH_WORLD_SIZE)
        self.aabb.add_point(self.pos - halfFinishSize)
        self.aabb.add_point(self.pos + halfFinishSize)

    def setpos(self, newpos):
        super(ColorVortex, self).setpos(newpos)
        for emitter in filter(lambda x: x.emitter, self.ps.actions):
            emitter.addPosDomain(CircleDomain(newpos, 0.1))

        self.resetaabb()

    def __init__(self, pos):
        super(FinishObject, self).__init__()
        self.pos = pos
        self.resetaabb()

        self.frame = 0
        self.elapsed = 0.0

        self.ps = ParticleSystem(50)
        emitter = EmitAction(15.0)
        emitter.addPosDomain(CircleDomain(self.pos, 0.27))
        emitter.addVelDomain(CircleDomain(Vector2(0.0, 1.5), 0.7))
        emitter.addColorDomain(SphereDomain(Vector3(160.0, 160.0, 160.0), 50.0))

        self.ps.addAction(emitter)
        self.ps.addAction(ForceAction(Vector2(0.0, -3.0)))
        self.ps.addAction(SpinAction(230.0))
        self.ps.addAction(MoveAction())
        self.ps.addAction(FadeAction(170.0))
        self.ps.addAction(KillFadedAction())

    def process(self, dt):
        self.ps.process(dt)

    def render(self, surface, campos):
        super(FinishObject, self).render(surface, campos)

        self.ps.render(surface, campos)
        
        renderPos = world2screenPos(campos, self.pos)
        finishScreenSize = int(world2screen(FINISH_WORLD_SIZE))
        renderPos.x -= int(0.5 * finishScreenSize)
        renderPos.y -= int(0.5 * finishScreenSize)
        renderRect = pygame.Rect(renderPos, (finishScreenSize, finishScreenSize))

        surface.blit(FinishObject.sprite, renderRect)

    def accept(self, event):
        pass

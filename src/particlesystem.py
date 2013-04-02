################################################################################
################################################################################
#
# particlesystem.py
#
# This file contains the basic implementation of a particle system.
#
################################################################################

import pygame, sys, random, math
from lib.euclid import *
from gameobject import *
from utils import *

class ParticleDomain(object): 

    def __init__(self):
        pass

    # Generate a random point within this domain
    def random(self):
        pass

    # Test whether or not the point is within the domain
    def within(self, pt):
        pass

class CircleDomain(ParticleDomain):
    def __init__(self, center, radius):
        super(ParticleDomain, self).__init__()
        self.center = center
        self.radius = radius

    def random(self):
        randomr = random.random()
        randomr = math.sqrt(randomr) * self.radius
        a = random.random() * 2 * math.pi

        dx = randomr * math.cos(a)
        dy = randomr * math.sin(a)

        return self.center + Vector2(dx, dy)

    def within(self, pos):
        return (self.center - pos).magnitude < self.radius

class PointDomain(ParticleDomain):
    def __init__(self, pt):
        super(ParticleDomain, self).__init__()
        self.pt = pt

    def random(self):
        return self.pt

    def within(self, pos):
        return (self.pt - pos).magnitude < 1e-6

class Particle(object):

    def __init__(self, sprite):
        self.sprite = sprite
        self.colorImage = pygame.Surface((1, 1), pygame.SRCALPHA, 32)
        self.colorImage = self.colorImage.convert_alpha()
        self.reinit()

    def reinit(self):
        self.__color = Vector3(255.0, 255.0, 255.0)
        self.__alpha = 255.0
        self.updateColor()

        self.pos = Vector2(0, 0)
        self.vel = Vector2(0, 0)
        self.lastupdate = -1
        self.mass = 1.0
        self.alive = False
        self.angle = 0.0
        self.size = 0.25

    def updateColor(self):
        color = self.color
        alpha = self.alpha
        c = pygame.Color(int(color.x), int(color.y), int(color.z), int(alpha))
        self.colorImage.fill(c)

    def setColor(self, color):

        self.__color.x = clamp(color.x, 0.0, 255.0)
        self.__color.y = clamp(color.y, 0.0, 255.0)
        self.__color.z = clamp(color.z, 0.0, 255.0)

        self.updateColor()

    def getColor(self):
        return self.__color
    
    def delColor(self):
        del self.__color

    def setAlpha(self, alpha):
        self.__alpha = clamp(alpha, 0.0, 255.0)
        self.updateColor()

    def getAlpha(self):
        return self.__alpha
    
    def delAlpha(self):
        del self.__alpha

    color = property(getColor, setColor, delColor, "Particle color")
    alpha = property(getAlpha, setAlpha, delAlpha, "Particle alpha")

    def printNumTranslucentPixels(self, surface, szx, szy):
        print "Num transparent: " + str(
            len(
                filter(
                    lambda x: x.a > 0 and x.a < 255, 
                    [surface.get_at((x, y)) for x in range(szx) for y in range(szy)])))
        
    def render(self, surface, campos):

        if not self.alive:
            return
        
        # Figure out the size of the sprite in pixels:
        ssz = int(world2screen(self.size))

        # Scale it based on this size and apply the color mask
        final = pygame.transform.scale(self.sprite, (ssz, ssz))
        finalcolor = pygame.transform.scale(self.colorImage, (ssz, ssz))

        final.blit(finalcolor, (0, 0), None, pygame.BLEND_RGBA_MULT)

        # Rotate it by the correct angle...
        final = pygame.transform.rotate(final, self.angle)

        # Draw it at the center of its rectangle..
        r = final.get_rect()
        w = r.width
        h = r.height
        c = world2screenPos(campos, self.pos)

        r.left = c.x - (h * 0.5)
        r.top = c.y - (w * 0.5)
        surface.blit(final, r)

class ParticleAction(object):
    
    def __init__(self):
        self.emitter = False

    # Perform an action on a particle....
    def act(self, particle, time):
        pass

class EmitAction(ParticleAction):

    def __init__(self, rate):
        super(EmitAction, self).__init__()
        self.rate = float(rate)
        self.numDead = 0
        self.emitter = True

    def addPosDomain(self, d):
        self.posDomain = d

    def addVelDomain(self, d):
        self.velDomain = d

    def addColorDomain(self, d):
        self.colDomain = d

    def act(self, particle, time):
        if particle.alive:
            return

        freq = self.rate / self.numDead
        if random.random() < freq:
            particle.alive = True
            particle.lastupdate = time

            if self.posDomain != None:
                particle.pos = self.posDomain.random()

            if self.velDomain != None:
                particle.vel = self.velDomain.random()

            if self.colDomain != None:
                particle.color = self.colDomain.random()

class KillAction(ParticleAction):
    def __init__(self, domain):
        super(KillAction, self).__init__()
        self.domain = domain

    def act(self, particle, time):
        if self.domain.within(particle.pos):
            particle.alive = False

class ForceAction(ParticleAction):
    def __init__(self, force):
        super(ForceAction, self).__init__()
        self.force = force

    def act(self, particle, time):
        dt = time - particle.lastupdate
        if dt <= 0:
            return

        a = self.force / particle.mass
        particle.vel += a * dt

class MoveAction(ParticleAction):
    def __init__(self):
        super(MoveAction, self).__init__()

    def act(self, particle, time):
        dt = time - particle.lastupdate
        if dt <= 0:
            return

        particle.pos += dt * particle.vel

class FadeAction(ParticleAction):
    def __init__(self, rate):
        super(FadeAction, self).__init__()
        self.rate = rate

    def act(self, particle, time):

        if not particle.alive:
            return

        dt = time - particle.lastupdate
        if dt <= 0:
            return

        particle.alpha -= dt * self.rate

class ParticleSystem(GameObject):

    def __init__(self, maxParticles, sprite="star"):
        
        super(ParticleSystem, self).__init__()

        # Load sprite image and setup some basic
        # animation parameters
        spriteFileName = os.sep.join([getRootPath(), "assets"]) + os.sep + sprite + ".png"
        spriteImage = pygame.image.load(spriteFileName)
        self.particles = [Particle(spriteImage) for i in range(maxParticles)]
        self.actions = []
        self.maxParticles = maxParticles

    # Emits a particle stochastically with the given rate. We know that we will reach
    # the maximum number of particles if we don't kill any with the given rate. Hence,
    # if we haven't reached the maximum number, simply do a dice roll to see if we should
    # generate one this frame.
    def addAction(self, action):
        self.actions.append(action)

    def process(self, time):

        # Make sure to update all emitters...
        dead = filter(lambda y: not y.alive, self.particles)
        for action in self.actions:
            if action.emitter:
                action.numDead = len(dead)

        for action in self.actions:
            for particle in self.particles:
                action.act(particle, time)

        for particle in self.particles:
            particle.lastupdate = time

    def render(self, time, surface, campos):
        
        self.process(time)

        for particle in self.particles:
            if particle.alive:
                particle.render(surface, campos)
        

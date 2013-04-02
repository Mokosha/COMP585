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
        randomr = math.sqrt(randomr)
        a = random.random() * 2 * math.pi

        dx = randomr * math.cos(a)
        dy = randomr * math.sin(a)

        return self.center + Vector2(dx, dy)

    def within(self, pos):
        return (self.center - pos).magnitude < self.radius

class Particle(object):

    def __init__(self, sprite):
        self.sprite = sprite
        self.colorImage = pygame.Surface((1, 1))
        self.setColor(pygame.Color(255, 255, 255, 255))
        self.pos = Vector2(0, 0)
        self.vel = Vector2(0, 0)
        self.lastupdate = -1
        self.mass = 1.0
        self.alive = False
        self.angle = 0.0
        self.size = 0.1

    def setColor(self, color):
        self.color = color
        self.colorImage.fill(self.color)

    def render(self, surface, campos):
        
        # Figure out the size of the sprite in pixels:
        ssz = int(world2screen(self.size))

        # Scale it based on this size and apply the color mask
        final = pygame.transform.scale(self.sprite, (ssz, ssz))
        finalcolor = pygame.transform.scale(self.colorImage, (ssz, ssz))

        final.blit(finalcolor, (0, 0))

        # Rotate it by the correct angle...
        final = pygame.transform.rotate(final, self.angle)

        # Draw it at the center of its rectangle..
        r = final.get_rect()
        w = r.width
        h = r.height
        c = world2screenPos(campos, self.pos)

        r.top = c.x - (h * 0.5)
        r.left = c.y - (w * 0.5)
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

    def act(self, particle, time):
        if not particle.alive:
            return

        freq = self.rate / self.numDead
        if random.random() < freq:
            particle.alive = True
            particle.lastupdate = time

            if self.posDomain != None:
                particle.pos = self.posDomain.random()

            if self.velDomain != None:
                particle.vel = self.velDomain.random()

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

        f = (self.force * dt) / particle.mass
        particle.vel += f

class MoveAction(ParticleAction):
    def __init__(self):
        super(MoveAction, self).__init__()

    def act(self, particle, time):
        dt = time - particle.lastupdate
        if dt <= 0:
            return

        particle.pos += dt * particle.vel

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
        

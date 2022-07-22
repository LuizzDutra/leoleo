import pygame as pg
from random import randint
from math import atan2, cos, sin
from time import time
from utils import remove_items_left_to_right


#objeto da particula que sera usado um conjunto
#do manuseador de partículas
class Particle:
    def __init__(self, pos:list, radius:int, direction:tuple, speed:int ,lifeTime:int, color, glow = False, glowIntensity = 1.5, vanish = True):
        self.surf = pg.Surface((radius*2, radius*2))
        self.surf.set_colorkey((0,0,0))
        self.color = color
        self.glowIntensity = glowIntensity
        self.radius = radius
        if glow:
            self.glow_color = (color[0]/2 , color[1]/2 , color[2]/2)
            self.glow = pg.Surface((radius*2 * glowIntensity, radius*2 * glowIntensity))
            self.glow.set_colorkey((0,0,0))
            pg.draw.circle(self.glow, self.glow_color, (self.glow.get_width()/2, self.glow.get_height()/2), radius * glowIntensity)
        pg.draw.circle(self.surf, color, (self.surf.get_width()/2, self.surf.get_height()/2), radius)
        self.sizeModifier = 1
        self.pos = list(pos)
        self.speed = speed
        self.creationTime = time()
        self.lifeTime = lifeTime
        angle = -atan2(direction[1], direction[0])
        self.xdir = cos(angle)
        self.ydir = sin(angle)
        self.vanish = vanish
       # print(self.xdir, self.ydir)
        self.last = time()
        self.dt = time() - self.last
    def update(self):
        self.dt = time() - self.last
        self.last = time()
        #movimento usando vetores
        self.pos[0] += self.xdir * self.dt * self.speed
        self.pos[1] += self.ydir * self.dt * self.speed
        if self.vanish: #caso ela vá diminuindo de tamanho
            #fórmula do modificador de tamanho baseado no tempo
            self.sizeModifier = ((self.lifeTime + self.creationTime) - time()) / self.lifeTime
            self.surf.fill((0,0,0))
            pg.draw.circle(self.surf, self.color, (self.surf.get_width()/2, self.surf.get_height()/2), self.radius * self.sizeModifier)
            if self.glow:
                self.glow.fill((0,0,0))
                pg.draw.circle(self.glow, self.glow_color, (self.glow.get_width()/2, self.glow.get_height()/2), self.radius * self.glowIntensity * self.sizeModifier)



class Particles_Handler:
    def __init__(self, particleLimit = 50):
        self.particles = []
        self.particleLimit = particleLimit

    def emit(self):
        for particle in self.particles:
            particle.update()

    def add(self, pos, radius, direction, speed, lifeTime, color = (255,255,255), glow = False, glowIntensity = 1.5, vanish = False):
        self.particles.append(Particle(pos, radius, direction, speed, lifeTime, color, glow = glow, glowIntensity = glowIntensity, vanish=vanish))
    
    def add_explosion(self, pos, radius, speed, lifeTime, intensity = 1, color = (255,255,255), glow = True, glowIntensity = 1.5, vanish=True):
        for i in range(intensity*10):
            randDir = (randint(-10, 10)/10, randint(-10, 10)/10)
            self.particles.append(Particle(pos, radius, randDir, speed, lifeTime, color, glow = glow, glowIntensity = glowIntensity, vanish=vanish))

    def delete(self):
        for particle in self.particles:
            if time() - particle.creationTime > particle.lifeTime:
                self.particles.remove(particle)
        if len(self.particles) > self.particleLimit:
            self.particles = remove_items_left_to_right(self.particles, len(self.particles) - self.particleLimit)

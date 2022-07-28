from turtle import back
import pygame as pg
from random import randint
from math import atan2, cos, sin
from time import time
from utils import remove_items_left_to_right


#objeto da particula que sera usado um conjunto
#do manuseador de partículas
class ParticleCircle:
    def __init__(self, pos:list, radius:int, direction:tuple, speed:int ,lifeTime: float, color, glow = False,
                 glowIntensity = 1.5, vanish = True, backLayer = False):
        self.surf = pg.Surface((radius*2, radius*2))
        self.surf.set_colorkey((0,0,0))
        self.color = color
        self.glowIntensity = glowIntensity
        self.radius = radius
        self.glows = glow #indica se brilha
        self.backLayer = backLayer #variavel que define se a partícula renderiza atrás ou na frente do sprite
        if glow:
            self.glow_color = (color[0]/2 , color[1]/2 , color[2]/2)
            self.glow = pg.Surface((radius*2 * glowIntensity, radius*2 * glowIntensity))
            self.glow.set_colorkey((0,0,0))
            pg.draw.circle(self.glow, self.glow_color, (self.glow.get_width()/2, self.glow.get_height()/2),
                           radius * glowIntensity)
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
            pg.draw.circle(self.surf, self.color, (self.surf.get_width()/2, self.surf.get_height()/2),
                           self.radius * self.sizeModifier)
            if self.glows:
                self.glow.fill((0,0,0))
                pg.draw.circle(self.glow, self.glow_color, (self.glow.get_width()/2, self.glow.get_height()/2),
                               self.radius * self.glowIntensity * self.sizeModifier)


class ParticleSquare:
    def __init__(self, pos: list, radius: int, direction: tuple, speed: int, lifeTime: float, color, glow=False,
                 glowIntensity=1.5, vanish=True, backLayer=False):
        self.surf = pg.Surface((radius * 2, radius * 2))
        self.surf.set_colorkey((0, 0, 0))
        self.surf.fill(color)
        self.radius = radius
        self.color = color
        self.glowIntensity = glowIntensity
        self.glows = glow  # indica se brilha
        self.backLayer = backLayer  # variável que define se a partícula renderiza atrás ou na frente do sprite
        if glow:
            self.glow_color = (color[0] / 2, color[1] / 2, color[2] / 2)
            self.glow = pg.Surface((radius * 2 * glowIntensity, radius * 2 * glowIntensity))
            self.glow.set_colorkey((0, 0, 0))
            pg.draw.circle(self.glow, self.glow_color, (self.glow.get_width() / 2, self.glow.get_height() / 2),
                           radius * glowIntensity)
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
        # movimento usando vetores
        self.pos[0] += self.xdir * self.dt * self.speed
        self.pos[1] += self.ydir * self.dt * self.speed
        if self.vanish:  # caso ela vá diminuindo de tamanho
            # fórmula do modificador de tamanho baseado no tempo
            self.sizeModifier = ((self.lifeTime + self.creationTime) - time()) / self.lifeTime
            self.surf = pg.transform.scale(self.surf, (self.radius * 2 * self.sizeModifier,
                                                       self.radius * 2 * self.sizeModifier))
            if self.glows:
                self.glow.fill((0, 0, 0))
                pg.draw.circle(self.glow, self.glow_color, (self.glow.get_width() / 2, self.glow.get_height() / 2),
                               self.radius * self.glowIntensity * self.sizeModifier)


class ParticleImage:
    def __init__(self, image: pg.Surface, pos: list, radius: int, direction: tuple, speed: int, lifeTime: float,
                 color=(0, 0, 0), glow=False, glowIntensity=1.5, vanish=True, backLayer=False):
        self.surf = pg.transform.scale(image,
                                       (radius * 2, radius * 2))
        self.radius = radius
        self.color = color
        self.glowIntensity = glowIntensity
        self.glows = glow  # indica se brilha
        self.backLayer = backLayer  # variável que define se a partícula renderiza atrás ou na frente do sprite
        if glow:
            self.glow_color = (color[0] / 2, color[1] / 2, color[2] / 2)
            self.glow = pg.Surface((radius * 2 * glowIntensity, radius * 2 * glowIntensity))
            self.glow.set_colorkey((0, 0, 0))
            pg.draw.circle(self.glow, self.glow_color, (self.glow.get_width() / 2, self.glow.get_height() / 2),
                           radius * glowIntensity)
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
        # movimento usando vetores
        self.pos[0] += self.xdir * self.dt * self.speed
        self.pos[1] += self.ydir * self.dt * self.speed
        if self.vanish:  # caso ela vá diminuindo de tamanho
            # fórmula do modificador de tamanho baseado no tempo
            self.sizeModifier = ((self.lifeTime + self.creationTime) - time()) / self.lifeTime
            if self.sizeModifier < 0:
                self.sizeModifier = 0
            self.surf = pg.transform.scale(self.surf,
                                           (self.radius * 2 * self.sizeModifier, self.radius * 2 * self.sizeModifier))
            if self.glows:
                self.glow.fill((0, 0, 0))
                pg.draw.circle(self.glow, self.glow_color, (self.glow.get_width() / 2, self.glow.get_height() / 2),
                               self.radius * self.glowIntensity * self.sizeModifier)



class Particles_Handler:
    def __init__(self, particleLimit = 50):
        self.particles = []
        self.particleLimit = particleLimit

    def emit(self):
        for particle in self.particles:
            particle.update()

    def add(self, pos, radius, direction, speed, lifeTime, color = (255,255,255), glow = False, glowIntensity = 1.5,
            vanish=False, backLayer=False, circle=False):
        if circle:
            self.particles.append(
                ParticleCircle(pos, radius, direction, speed, lifeTime, color, glow=glow, glowIntensity=glowIntensity,
                               vanish=vanish, backLayer=backLayer))
        else:
            self.particles.append(
                ParticleSquare(pos, radius, direction, speed, lifeTime, color, glow=glow, glowIntensity=glowIntensity,
                               vanish=vanish, backLayer=backLayer))
    
    def add_explosion(self, pos, radius, speed, lifeTime, intensity = 1, color = (255,255,255), glow=True,
                      glowIntensity = 1.5, vanish=True, backLayer = False, circle=False):
        for i in range(int(intensity*10)):
            randDir = (randint(-10, 10)/10, randint(-10, 10)/10)
            randSpeed = randint(int(speed - int(speed/2)), int(speed + int(speed/2)))
            if circle:
                self.particles.append(ParticleCircle(pos, radius, randDir, randSpeed, lifeTime, color, glow=glow,
                                                     glowIntensity=glowIntensity, vanish=vanish, backLayer=backLayer))
            else:
                self.particles.append(ParticleSquare(pos, radius, randDir, randSpeed, lifeTime, color, glow=glow,
                                                     glowIntensity=glowIntensity, vanish=vanish, backLayer=backLayer))

    def add_image(self, image: pg.Surface, pos, radius, direction, speed, lifeTime, color=(255, 255, 255), glow = False,
                  glowIntensity=1.5, vanish=False, backLayer=False, circle=False):
        self.particles.append(
            ParticleImage(image, pos, radius, direction, speed, lifeTime, color, glow=glow, glowIntensity=glowIntensity,
                           vanish=vanish, backLayer=backLayer))

    def add_image_explosion(self, image: pg.Surface, pos, radius, speed, lifeTime, intensity,
                            color=(64, 64, 64), glow=False, glowIntensity=1.5, vanish=True,
                            backLayer=False, circle=False):
        for i in range(int(intensity*10)):
            randdir = (randint(-10, 10)/10, randint(-10, 10)/10)
            randspeed = randint(int(speed - int(speed / 2)), int(speed + int(speed / 2)))
            self.particles.append(
                ParticleImage(image, pos, radius, randdir, randspeed, lifeTime, color, glow=glow,
                              glowIntensity=glowIntensity, vanish=vanish, backLayer=backLayer))

    def delete(self):
        for particle in self.particles:
            if time() - particle.creationTime > particle.lifeTime:
                self.particles.remove(particle)
        if len(self.particles) > self.particleLimit:
            self.particles = remove_items_left_to_right(self.particles, len(self.particles) - self.particleLimit)

    def clear(self):
        self.particles.clear()


impactCreator = Particles_Handler(500)

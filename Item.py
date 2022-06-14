import pygame as pg
import os
from time import time

ball_group = pg.sprite.Group()

sprites = []
sprites.append(pg.Surface((0, 0)))
sprites.append(pg.transform.scale(pg.image.load(os.path.join("Assets", "ball.png")), (32,32)))
sprites.append(pg.Surface((32,32)))
sprites.append(pg.Surface((32,32)))
sprites.append(pg.Surface((32,32)))
sprites.append(pg.Surface((32,32)))
sprites.append(pg.Surface((32,32)))
errorimage = pg.Surface((32,32))
errorimage.fill((255,0,150))

class Item(pg.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.name = "Unasigned"
		self.image = errorimage
		self.rect = self.image.get_rect()
	def use(self, player:pg.sprite.Sprite):
		print("Define the use function idiot")
		print(type(self))
		self.remove_from_list(player.inv_list)
		
	def remove_from_list(self, list=[]):
		for i, item in enumerate(list):
			if item == self:
				list[i] = None



class Paper_Ball(Item):
	def __init__(self):
		super().__init__()
		self.name = "Ball"
		self.image = sprites[1]
		self.rect = self.image.get_rect()
	def use(self, player):
		if player.energy >= 5:
			ball_group.add(Ball(player))
			player.energy -= 5
			self.remove_from_list(player.inv_list)


class Manguza(Item):
	def __init__(self):
		super().__init__()
		self.name = "Manguzá"
		self.image = sprites[2]
		self.rect = self.image.get_rect()
	def use(self, player):
		player.energy += 15
		self.remove_from_list(player.inv_list)

class Pacoca(Item):
	def __init__(self):
		super().__init__()
		self.name = "Paçoca"
		self.image = sprites[3]
	def use(self, player):
		player.energy += 10
		self.remove_from_list(player.inv_list)

#Essa classe é um projétil e não item
class Ball(pg.sprite.Sprite): #https://www.youtube.com/watch?v=JmpA7TU_0Ms
	def __init__(self, player):
		super().__init__()
		self.sprites = []
		self.sprites.append(pg.transform.scale(pg.image.load(os.path.join("Assets", "ball.png")), (16,16)))
		self.image = self.sprites[0]
		self.rect = self.image.get_rect(center = player.rect.center)
		self.speed = 10
		self.xdir = 0
		self.ydir = 0
		if player.xvel > 0:
			self.xdir = 1
		if player.xvel < 0:
			self.xdir = -1
		if player.yvel > 0:
			self.ydir = 1
		if player.yvel < 0:
			self.ydir = -1
		self.time = time()
		self.life_time = 5

	def update(self):
		self.rect.x += self.speed * self.xdir
		self.rect.y += self.speed * self.ydir
		if time() - self.time > self.life_time:
			self.kill()
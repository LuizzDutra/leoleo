import pygame as pg
import os
from time import time

ball_group = pg.sprite.Group()
drop_item_group = pg.sprite.Group()

class Item():
	def __init__(self, id=0):
		self.sprites = []
		self.sprites.append(pg.Surface((0, 0)))
		self.sprites.append(pg.transform.scale(pg.image.load(os.path.join("Assets", "ball.png")), (32,32)))
		self.sprites.append(pg.Surface((32,32)))
		self.sprites[2].fill((0,150,0))
		self.name_dict = {0:"none", 1:"ball", 2:"Car"}
		self.id = id
		try:
			self.image = self.sprites[self.id]
		except:
			self.id = 0
			self.image = self.sprites[self.id]
		self.rect = self.image.get_rect()
	def drop(self, pos):
		if self.id != 0:
			drop_item_group.add(self.Drop_Item(pos,self.sprites[self.id] , self.id))
			self.id = 0
	def use(self, player):
		if self.id == 1:
			if player.xvel or player.yvel != 0 and player.energy >= 5:
				Ball.ball_throw(player)
				player.energy -= 5
				self.id = 0
		if self.id == 2:
			player.energy += 10
			self.id = 0
	def update(self):
		self.image = self.sprites[self.id]
		self.rect = self.image.get_rect()
		self.name = self.name_dict[self.id]
	class Drop_Item(pg.sprite.Sprite):
		def __init__(self, pos, image, id=0):
			super().__init__()
			self.id = id
			self.image = pg.transform.scale(image, (16,16))
			self.rect = self.image.get_rect(center = pos)
		def interact(self, item_list):
			for slot in item_list:
				if slot.id == 0:
					slot.id = self.id
					self.kill()
					break

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

	def ball_throw(player_pos):
		ball_group.add(Ball(player_pos))

	def update(self):
		self.rect.x += self.speed * self.xdir
		self.rect.y += self.speed * self.ydir
		if time() - self.time > self.life_time:
			self.kill()
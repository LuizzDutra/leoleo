import pygame as pg
import os

class Player(pg.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.sprites = []
		self.sprites.append(pg.transform.scale(pg.image.load(os.path.join("Assets", "bob.png")), (32, 32)))
		self.image = self.sprites[0]
		self.rect = self.image.get_rect(center = (0, 0))
		self.xspeed = 5
		self.yspeed = 5
		self.xvel = 0
		self.yvel = 0
		self.use_delay = 0.2
		self.last_use = 0
		self.inv_select = 0
		self.item_list = []
		self.energy_max = 100
		self.energy = 100
		self.hp_max = 100
		self.hp = 100

	def update(self):
		if self.energy > self.energy_max:
			self.energy = self.energy_max
		if self.hp > self.hp_max:
			self.hp = self.hp_max
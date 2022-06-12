import pygame as pg
import os
from time import time

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
		self.pickup_range = 100
		self.interactable_list = []
	def control(self, keys_pressed):
		self.xvel = 0
		self.yvel = 0
		if keys_pressed[pg.K_a]:
			self.xvel = -self.xspeed
		if keys_pressed[pg.K_d]:
			self.xvel = +self.xspeed
		if keys_pressed[pg.K_w]:
			self.yvel = -self.yspeed
		if keys_pressed[pg.K_s]:
			self.yvel = +self.yspeed
		if keys_pressed[pg.K_LSHIFT]:
			self.xvel *= 0.5
			self.yvel *= 0.5
		self.rect.x += self.xvel
		self.rect.y += self.yvel
		if keys_pressed[pg.K_f]:
			if (time() - self.last_use) > self.use_delay:
				self.item_list[self.inv_select].use(self)
				self.last_use = time()
		if keys_pressed[pg.K_g]:
			self.item_list[self.inv_select].drop(self.rect.center)
		if keys_pressed[pg.K_e]:
			if (time() - self.last_use) > self.use_delay:
				self.interact()
				self.last_use = time()
		if keys_pressed[pg.K_1]:
			self.inv_select = 0
		if keys_pressed[pg.K_2]:
			self.inv_select = 1
		if keys_pressed[pg.K_3]:
			self.inv_select = 2
		if keys_pressed[pg.K_4]:
			self.inv_select = 3
		if keys_pressed[pg.K_5]:
			self.inv_select = 4
		if keys_pressed[pg.K_t]:
			for item in self.item_list:
				if item.id  == 0:
					item.id = 1
	def get_interactable_list(self, item_group = pg.sprite.Group, interactable_group_list = []):
		self.interactable_list = [] #reset da lista
		#interação do personagem/ for loop usado para filtrar os interagiveis por distância.
		#Objetos no alcançe são colocados em uma lista de interação
		for i in range(10, 0, -1):
			for item in item_group:
				if abs(self.rect.x - item.rect.center[0]) < self.pickup_range/i and abs(self.rect.y - item.rect.center[1]) < self.pickup_range/i:
					if len(self.interactable_list) == 0:
						self.interactable_list.append(item)
			for group in interactable_group_list:
					for obj in group:
						if abs(self.rect.x - obj.rect.center[0]) < self.pickup_range/i and abs(self.rect.y - obj.rect.center[1]) < self.pickup_range/i:
							if len(self.interactable_list) == 0:
								self.interactable_list.append(obj)

	def interact(self):
		for obj in self.interactable_list:
			try:
				obj.interact(self.item_list)
			except:
				obj.interact()
	def update(self):

		if self.energy > self.energy_max:
			self.energy = self.energy_max
		if self.hp > self.hp_max:
			self.hp = self.hp_max
		for item in self.item_list:
			item.update()
import pygame as pg
import images
from time import time
from item import Item, Paper_Ball


drop_item_group = pg.sprite.Group()

class Player(pg.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.sprites = []
		self.sprites.append(images.player_image)
		self.image = self.sprites[0]
		self.rect = self.image.get_rect(center = (0, 0))
		self.xspeed = 5
		self.yspeed = 5
		self.xvel = 0
		self.yvel = 0
		self.use_delay = 0.2
		self.last_use = 0
		self.inv_select = 0
		self.inv_limit = 5
		self.inv_list = []
		self.energy_max = 100
		self.energy = 100
		self.hp_max = 100
		self.hp = 100
		self.money = 0
		self.pickup_range = 48
		self.interactable_list = []
	def control(self, keys_pressed):
		self.xvel = 0
		self.yvel = 0
		if keys_pressed[pg.K_a]:
			self.xvel -= self.xspeed
		if keys_pressed[pg.K_d]:
			self.xvel += self.xspeed
		if keys_pressed[pg.K_w]:
			self.yvel -= self.yspeed
		if keys_pressed[pg.K_s]:
			self.yvel += self.yspeed
		if keys_pressed[pg.K_LSHIFT]:
			self.xvel /= 2
			self.yvel /= 2
		self.rect.x += self.xvel
		self.rect.y += self.yvel
		if keys_pressed[pg.K_f]:
			if (time() - self.last_use) > self.use_delay:
				self.use_item(self.inv_list[self.inv_select])
				self.last_use = time()
		if keys_pressed[pg.K_g]:
			self.drop_item(drop_item_group)
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
			for i, item in enumerate(self.inv_list):
				if item == None:
					self.inv_list[i] = Paper_Ball()
	def get_interactable_list(self, item_group:pg.sprite.Group, interactable_group_list = []):
		self.interactable_list = [] #reset da lista
		#interação do personagem/ for loop usado para filtrar os interagiveis por distância.
		#Objetos no alcançe são colocados em uma lista de interação
		for i in range(10, 0, -1):
			for group in interactable_group_list:
					for obj in group:
						if abs(self.rect.centerx - obj.rect.center[0]) < self.pickup_range/i and abs(self.rect.centery - obj.rect.center[1]) < self.pickup_range/i:
							if len(self.interactable_list) == 0:
								self.interactable_list.append(obj)
			for item in item_group:
				if abs(self.rect.centerx - item.rect.center[0]) < self.pickup_range/i and abs(self.rect.centery - item.rect.center[1]) < self.pickup_range/i:
					if len(self.interactable_list) == 0:
						self.interactable_list.append(item)


	def add_item(self, item:pg.sprite.Sprite):
		if len(self.inv_list) < self.inv_limit:
			item.kill()
			self.inv_list.append(item)
			return
		for i, slot in enumerate(self.inv_list):
			if slot == None:
				item.kill()
				self.inv_list[i] = item
				return
	def drop_item(self, group:pg.sprite.Group):
		if self.inv_list[self.inv_select] != None:
			self.inv_list[self.inv_select].rect.center = self.rect.center
			group.add(self.inv_list[self.inv_select])
			self.inv_list[self.inv_select] = None
	def use_item(self, item:pg.sprite.Sprite):
		if item != None:
			item.use(self)
	def interact(self):
		for obj in self.interactable_list:
			if isinstance(obj, Item):
				self.add_item(obj)
			else:
				#print(type)
				obj.interact()

	def update(self):
		if self.energy > self.energy_max:
			self.energy = self.energy_max
		if self.hp > self.hp_max:
			self.hp = self.hp_max
		while len(self.inv_list) < self.inv_limit:
			self.inv_list.append(None)

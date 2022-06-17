import pygame as pg
from time import time
import images
import sons
#Decidi que a escala vai ser 64p:1m
gs = 32 #cada grid tem meio metro

class Wall(pg.sprite.Sprite):
	def __init__(self, pos:tuple, id):
		super().__init__()
		self.image = images.wall_list[id]
		self.rect = self.image.get_rect(center = (pos[0]*gs , pos[1]*gs))

class Door(pg.sprite.Sprite):
	def __init__(self, x, y, width, height, locked=False, id = 0, closed = True):
		super().__init__()
		if width > height:
			self.image = pg.transform.scale(images.door, (width*gs, height*gs))
			self.vertical = False
		if width < height:
			self.image = pg.transform.scale(pg.transform.rotate(images.door, (-90)), (width*gs, height*gs))
			self.vertical = True
		if width == height:
			self.image = pg.transform.scale(images.door, (width*gs, height*gs))
			self.vertical = True
		self.rect = self.image.get_rect(x = x*gs, y = y*gs)
		self.open_time = 0.5
		self.open_delta = 0
		self.locked = locked
		self.id = id
		self.closed = closed

	def lock(self):
		if self.closed:
			self.locked = True
			sons.effect_play(sons.key)
	
	def unlock(self):
		self.locked = False
		sons.effect_play(sons.key)

	def lock_unlock(self):
		if self.locked:
			self.unlock()
		elif not self.locked:
			self.lock()

	def interact(self, rect):
		if time() - self.open_delta > self.open_time:
			if self.locked:
				sons.play_far_effect(rect, self.rect, sons.locked)
			if not self.locked:
				self.open_delta = time()
				if self.closed:
					if self.vertical:
						self.image = pg.transform.rotate(self.image, 90)
					if not self.vertical:
						self.image = pg.transform.rotate(self.image, -90)
					sons.play_far_effect(rect, self.rect, sons.open_dr)
				if not self.closed:
					if self.vertical:
						self.image = pg.transform.rotate(self.image, -90)
					if not self.vertical:
						self.image = pg.transform.rotate(self.image, 90)
					sons.play_far_effect(rect, self.rect, sons.cls_dr)
				self.rect = self.image.get_rect(x = self.rect.x, y = self.rect.y)
				self.closed = not self.closed


level0 = []
#11-21x 6y
#teste de criação de mapa
for i in range(11, 22):
	level0.append(Wall((i, 6), 0))
for i in range(11, 22):
	if i != 15 and i !=16 and i != 17:
	 level0.append(Wall((i, 16), 0))





def level_construct(wall_group, level):
    for wall in wall_group:
        wall.kill()
    for wall in level:
        wall_group.add(wall)
    return wall_group
import pygame as pg
from time import time
import images
#Decidi que a escala vai ser 64p:1m
gs = 64

class Wall(pg.sprite.Sprite):
	def __init__(self, pos:tuple, image):
		super().__init__()
		self.image = image
		self.rect = self.image.get_rect(x = pos[0]*gs , y = pos[1]*gs)

class Door(pg.sprite.Sprite):
	def __init__(self, x, y, width, height, locked=False, id = 0, closed = True):
		super().__init__()
		if width > height:
			self.image = pg.transform.scale(images.door, (width, height))
			self.vertical = False
		if width < height:
			self.image = pg.transform.scale(pg.transform.rotate(images.door, (-90)), (width, height))
			self.vertical = True
		if width == height:
			self.image = pg.transform.scale(images.door, (width, height))
			self.vertical = True
		self.rect = self.image.get_rect(x = x, y = y)
		self.open_time = 0.5
		self.open_delta = 0
		self.locked = locked
		self.id = id
		self.closed = closed

	def lock(self):
		if self.closed:
			self.locked = True
	
	def unlock(self):
		self.locked = False

	def lock_unlock(self):
		if self.locked:
			self.unlock()
		elif not self.locked:
			self.lock()

	def interact(self):
		if time() - self.open_delta > self.open_time:
			if not self.locked:
				self.open_delta = time()
				if self.closed:
					if self.vertical:
						self.image = pg.transform.rotate(self.image, 90)
					if not self.vertical:
						self.image = pg.transform.rotate(self.image, -90)
				if not self.closed:
					if self.vertical:
						self.image = pg.transform.rotate(self.image, -90)
					if not self.vertical:
						self.image = pg.transform.rotate(self.image, 90)
				self.rect = self.image.get_rect(x = self.rect.x, y = self.rect.y)
				self.closed = not self.closed


wall0 = Wall((1,1), images.twall_v)
wall1 = Wall((1,2), images.twall_h)



level0 = [wall0, wall1]

def level_construct(wall_group, level):
    for wall in wall_group:
        wall.kill()
    for wall in level:
        wall_group.add(wall)
    return wall_group
import pygame as pg
from time import time
import images
import sons
import groups
from PIL import Image
import os
from random import randint
#Decidi que a escala vai ser 64p:1m
gs = 32 #cada grid tem meio metro

#paleta vai estar aqui e não no mapa
BLACK = (0,0,0) #parede0
RED = (255,0,0) #parede1
GREEN = (0,255,0) #grama
BLUE = (0,0,255) #piso
YELLOW = (255,255,0)
PINK = (255,0,255)
CYAN = (0,255,255)

class Wall(pg.sprite.Sprite):
	def __init__(self, pos:tuple, id):
		super().__init__()
		self.image = images.wall_list[id]
		self.rect = self.image.get_rect(center = (pos[0]*gs , pos[1]*gs))

class Ground(pg.sprite.Sprite):
	def __init__(self, pos:tuple, id, rot=False):
		super().__init__()
		rot_dict = {0:90, 1:180, 2:270, 3:0}
		if rot:
			self.image = pg.transform.rotate(images.ground_list[id], rot_dict[randint(0, 3)])
		else:
			self.image = images.ground_list[id]
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

class Level_sprite(pg.sprite.Sprite):
	def __init__(self, image, x=0, y=0):
		super().__init__()
		self.image = pg.Surface((image.size[0]*gs, image.size[1]*gs))
		self.rect = self.image.get_rect(x = x, y = y)
class Level_partition_sprite(pg.sprite.Sprite):
	def __init__(self, image, x=0, y=0):
		super().__init__()
		self.image = image
		self.image.convert()
		self.rect = self.image.get_rect(x = x, y = y)



#teste de criação de mapa
level0 = Image.open(os.path.join("Assets", "level0.png"), "r")

#usado para debug, bem bugado
def reload_level():
	global level0
	level0 = Image.open(os.path.join("Assets", "level0.png"), "r")

def get_pallete(image:Image.Image) -> list:
	temp_pallete_list = image.getpalette()
	pallete_list = []
	for i in range(0, len(temp_pallete_list), 3):
		pallete_list.append((temp_pallete_list[i], temp_pallete_list[i+1],temp_pallete_list[i+2]))
	return pallete_list


def level_construct(level_image:Image.Image, part_quantity=36):
	print("Carrengando mapa")
	for surface in groups.level_surface_group:
		surface.kill()
	for wall in groups.wall_group:
		wall.kill()
	for ground in groups.ground_group:
		ground.kill()
	level_size = level_image.size
	level_surface = Level_sprite(level_image)
	level_surface.image.fill((50,50,50))
	pallete = get_pallete(level_image)

	for y in range(0, level_size[1]):
		for x in range(0, level_size[0]):
			if pallete[level_image.getpixel((x,y))] == BLACK:
					groups.wall_group.add(Wall((x, y), 0))
			if pallete[level_image.getpixel((x,y))] == RED:
				groups.wall_group.add(Wall((x,y), 1))
			if pallete[level_image.getpixel((x,y))] == GREEN:
					groups.ground_group.add(Ground((x, y), 0))
			if pallete[level_image.getpixel((x,y))] == BLUE:
				groups.ground_group.add(Ground((x,y), 1))
			
	for ground in groups.ground_group:
		level_surface.image.blit(ground.image, ground.rect.topleft)
	for wall in groups.wall_group:
		level_surface.image.blit(wall.image, wall.rect.topleft)

	level_width = level_surface.image.get_width()
	level_height = level_surface.image.get_height()
	rcq = int(part_quantity**(1/2)) #quantidades de colunas/linhas no quadrado
	i = 0
	for y in range(0,rcq):
		for x in range(0,rcq):
			temp_surface = pg.Surface((level_width/rcq, level_height/rcq))
			temp_surface.blit(level_surface.image, (-x*(level_width/rcq), -y*(level_height/rcq)))
			groups.level_surface_group.add(Level_partition_sprite(temp_surface, x*(level_width/rcq), y*(level_height/rcq)))
			i += 1
	print("O mapa particionado em {} partes".format(i))

	print("Mapa Carregado")
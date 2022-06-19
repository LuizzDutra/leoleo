import pygame as pg
import images
from math import atan2, cos, sin
from time import time
from utils import rfl
from lc import Door
from groups import ball_group
import sons



class Item(pg.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.name = "Unasigned"
		self.image = images.errorimage
		self.rect = self.image.get_rect()
	def use(self, player:pg.sprite.Sprite):
		print("Define the use function idiot")
		print(type(self))
		rfl(self, player.inv_list)

class Key(Item):
	def __init__(self, id:int):
		super().__init__()
		self.name = "Chave"
		self.image = images.chave
		self.rect = self.image.get_rect()
		self.id = id
	def use(self, player):
		for obj in player.interactable_list:
			if isinstance(obj, Door):
				if self.id == obj.id:
					obj.lock_unlock()

class Money(Item):
	def __init__(self, quantity:int):
		super().__init__()
		self.name = "Dinheiro"
		self.image = images.money
		self.rect = self.image.get_rect()
		self.quantity = quantity
	def use(self, player):
		player.money += self.quantity
		sons.effect_play(sons.cashing)
		rfl(self, player.inv_list)

class Paper_Ball(Item):
	def __init__(self):
		super().__init__()
		self.name = "Ball"
		self.image = images.bola_papel
		self.rect = self.image.get_rect()
	def use(self, player):
		if player.energy >= 5:
			ball_group.add(Ball(player))
			player.energy -= 5
			rfl(self, player.inv_list)
			sons.effect_play(sons.throw)


class Manguza(Item):
	def __init__(self):
		super().__init__()
		self.name = "Manguzá"
		self.image = images.manguza
		self.rect = self.image.get_rect()
	def use(self, player):
		player.energy += 15
		rfl(self, player.inv_list)

class Pacoca(Item):
	def __init__(self):
		super().__init__()
		self.name = "Paçoca"
		#self.image = sprites[3]
	def use(self, player):
		player.energy += 50
		rfl(self, player.inv_list)

#Essa classe é um projétil e não item
class Ball(pg.sprite.Sprite): #https://www.youtube.com/watch?v=JmpA7TU_0Ms
	def __init__(self, player:pg.sprite.Sprite):
		super().__init__()
		self.image = images.bola_papel_projetil
		self.rect = self.image.get_rect(center = player.rect.center)
		self.speed = 10
		self.xdir = 0
		self.ydir = 0
		m_ypos = (pg.mouse.get_pos()[1] - images.screen.get_height()/2)
		m_xpos = (pg.mouse.get_pos()[0] - images.screen.get_width()/2)
		self.angle = atan2(m_ypos, m_xpos)
		self.xdir = cos(self.angle) 
		self.ydir = sin(self.angle) 
		print(m_ypos)
		print(m_xpos)
		print(self.xdir)
		print(self.ydir)
		self.time = time()
		self.life_time = 5

	def update(self):
		self.rect.x += self.speed * self.xdir
		self.rect.y += self.speed * self.ydir
		if time() - self.time > self.life_time:
			self.kill()

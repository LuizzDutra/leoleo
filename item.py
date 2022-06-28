import pygame as pg
import images
from math import atan2, cos, sin
from random import randint
from utils import rfl
from lc import Door
from groups import ball_group, drop_item_group
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
		self.chave_name = "Chave "
		self.name_dict = {0 : "Mestra", 1 : "Comum"}
		if id in self.name_dict:
			self.name = self.chave_name + self.name_dict[id]
		else:
			self.name = self.chave_name + str(id)
		self.image = images.chave
		self.rect = self.image.get_rect()
		self.id = id
	def use(self, player):
		for obj in player.interactable_list:
			if isinstance(obj, Door):
				obj.lock_unlock(self.id)

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
		self.og_image = images.bola_papel_projetil
		self.image = self.og_image
		#aleatoriedade pra ficar mais orgânico
		self.rps = randint(1, 3) #rotações por segundo
		self.angle = 0
		self.rect = self.image.get_rect(center = player.rect.center)
		self.speed = float(6000)
		self.xspeed = self.speed
		self.yspeed = self.speed
		self.n_xspeed = self.xspeed
		self.n_yspeed = self.yspeed
		self.xpos = self.rect.x
		self.ypos = self.rect.y
		self.xdir = 0
		self.ydir = 0
		m_ypos = (pg.mouse.get_pos()[1] - images.screen.get_height()/2)
		m_xpos = (pg.mouse.get_pos()[0] - images.screen.get_width()/2)
		self.angle = atan2(m_ypos, m_xpos)
		self.xdir = cos(self.angle) 
		self.ydir = sin(self.angle) 
		self.time = pg.time.get_ticks()/1000
		self.life_time = 1
		self.dt = pg.time.get_ticks()/1000
		self.last = pg.time.get_ticks()/1000
		self.bounce_qt = 0 #quantidade de quicadas☺
		self.bounce_limit = 2
		self.last_bounce = 0
		self.dead = False
	def drop(self):
		self.kill()
		self.dead = True #usado para garantir que a bola não drope mais de uma vez em caso de múltiplas colisões
		drop = Paper_Ball()
		drop.rect.center = self.rect.center
		drop_item_group.add(drop)
	def bounce(self, rect:pg.Rect):
		if self.bounce_qt < self.bounce_limit:
			if abs(rect.bottom - self.rect.top) < self.yspeed*self.dt+5:
				self.yspeed *= -1
			if abs(rect.left - self.rect.right) < self.xspeed*self.dt+5:
				self.xspeed *= -1
			if abs(rect.right - self.rect.left) < self.xspeed*self.dt+5:
				self.xspeed *= -1
			if abs(rect.top - self.rect.bottom) < self.yspeed*self.dt+5:
				self.yspeed *= -1
			self.bounce_qt += 1
			self.life_time *= 0.75
			if pg.time.get_ticks()/1000 - self.last_bounce > 0.05:
				sons.play_far_effect(self.rect, sons.ball_hit)
			self.last_bounce = pg.time.get_ticks()/1000
		else:
			if not self.dead:
				self.drop()


	def update(self, player_rect):
		self.player_rect = player_rect #referência para som
		self.dt = pg.time.get_ticks()/1000 - self.last
		self.last = pg.time.get_ticks()/1000
		self.n_xspeed = self.xspeed * (self.life_time - (pg.time.get_ticks()/1000-self.time))/5
		self.n_yspeed = self.yspeed * (self.life_time - (pg.time.get_ticks()/1000-self.time))/5
		self.xpos += self.n_xspeed * self.dt * self.xdir
		self.ypos += self.n_yspeed * self.dt *self.ydir
		self.rect.x = round(self.xpos)
		self.rect.y = round(self.ypos)
		self.angle += self.rps*360*self.dt
		self.image = pg.transform.rotate(self.og_image, self.angle)
		if pg.time.get_ticks()/1000 - self.time > self.life_time:
			self.drop()
			


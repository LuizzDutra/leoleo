from cmath import atanh
import pygame as pg
import os, sys, math, time

class Player(pg.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.sprites = []
		self.sprites.append(pg.transform.scale(pg.image.load(os.path.join("Assets", "bob.png")), (64,64)))
		self.image = self.sprites[0]
		self.rect = self.image.get_rect(center = (screen_width/2, screen_height/2))
		self.speed = 5


	def ball_throw(self):
		return Ball(player.rect.center)

	def move(self):
		if keys_pressed[pg.K_a]:
			self.rect.x -= self.speed
		if keys_pressed[pg.K_d]:
			self.rect.x += self.speed
		if keys_pressed[pg.K_w]:
			self.rect.y -= self.speed
		if keys_pressed[pg.K_s]:
			self.rect.y += self.speed

	def update(self):
		self.move()


	

class Ball(pg.sprite.Sprite):
	def __init__(self, player_pos):
		super().__init__()
		self.sprites = []
		self.sprites.append(pg.transform.scale(pg.image.load(os.path.join("Assets", "ball.png")), (16,16)))
		self.image = self.sprites[0]
		self.rect = self.image.get_rect(center = player_pos)
		self.speed = 10
		self.angle = math.atan2(pg.mouse.get_pos()[1] - self.rect.y, pg.mouse.get_pos()[0] - self.rect.x)
		self.xdir = math.cos(self.angle) 
		self.ydir = math.sin(self.angle) 
		self.time = time.time()
		self.life_time = 5

	def md(self, n):
		if n < 0:
			n *= -1
		return n

	def update(self):
		self.rect.x += self.speed * self.xdir
		self.rect.y += self.speed * self.ydir
		if time.time() - self.time > self.life_time:
			self.kill()

pg.init()
screen_width, screen_height = 1280, 720
screen = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption("Oho")
clock = pg.time.Clock()
#pg.mouse.set_visible(False)

player = Player()
player_group = pg.sprite.Group()
player_group.add(player)

ball_group = pg.sprite.Group()


def draw():
	screen.fill((100,100,100))

	ball_group.draw(screen)
	player_group.draw(screen)
	
	pg.display.update()

while True:

	for event in pg.event.get():
		if event.type == pg.QUIT:
			pg.quit()
			sys.exit()
		if event.type == pg.MOUSEBUTTONDOWN:
			ball_group.add(player.ball_throw())
	
	keys_pressed = pg.key.get_pressed()

	player_group.update()
	ball_group.update()
	draw()

	clock.tick(60)

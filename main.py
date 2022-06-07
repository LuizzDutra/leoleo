import pygame as pg
import os, sys, time
import lc

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
		self.throw_delay = 1
		self.last_throw = 0

	def ball_throw(self):
		if time.time() - self.last_throw > self.throw_delay:
			self.last_throw = time.time()
			ball_group.add(Ball(self.rect.center))

	def move(self):
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

	def update(self):
		self.move()
	
class Ball(pg.sprite.Sprite): #https://www.youtube.com/watch?v=JmpA7TU_0Ms
	def __init__(self, player_pos):
		super().__init__()
		self.sprites = []
		self.sprites.append(pg.transform.scale(pg.image.load(os.path.join("Assets", "ball.png")), (16,16)))
		self.image = self.sprites[0]
		self.rect = self.image.get_rect(center = player_pos)
		self.speed = 10
		self.xdir = 0
		self.ydir = 0
		if keys_pressed[pg.K_d]:
			self.xdir = 1 
		if keys_pressed[pg.K_s]: 
			self.ydir = 1 
		if keys_pressed[pg.K_a]:
			self.xdir = -1 
		if keys_pressed[pg.K_w]: 
			self.ydir = -1 

		self.time = time.time()
		self.life_time = 5

	def update(self):
		self.rect.x += self.speed * self.xdir
		self.rect.y += self.speed * self.ydir
		if time.time() - self.time > self.life_time:
			self.kill()

#Classe de tempo que será usada para calcular o horário e passar os dias
class Time():
	def __init__(self):
		self.timescale = 10000 #Escala de tempo em relação à vida real/ padrão = 60
		self.start_time = time.time()
		self.cur_time = 0 #Tempo que passou desde a criaçãoo do objeto com a classe
		self.day = 1 #Use o operador "%" por 7 (ex:day % 7) no index do "week_day" para pegar o dia da semana/ Ex: dado day = 1 -> weekday[day%7] --> "Segunda"
		self.week_day = {0:"Domingo", 1:"Segunda", 2:"Terca", 3:"Quarta", 4:"Quinta", 5:"Sexta", 6:"Sabado"}
		self.day_duration = 34200
	
	def day_pass_check(self):
		if self.cur_time > self.day_duration:
			self.day += 1
			self.start_time = time.time()

	def update(self):
		self.day_pass_check()
		self.cur_time = (time.time() - self.start_time) * self.timescale
	
#Ponteiro personalizado
class Cursor(pg.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.sprites = []
		self.sprites.append(pg.image.load(os.path.join("Assets", "cursor.png")))
		self.image = self.sprites[0]
		self.rect = self.image.get_rect(center = pg.mouse.get_pos())
	def update(self):
		self.rect.center = pg.mouse.get_pos()

class Camera():
	def __init__(self):
		self.xoffset = screen_width/2 - player.rect.x;
		self.yoffset = screen_height/2 - player.rect.y;
	def update(self):
		self.xoffset = screen_width/2 - player.rect.x;
		self.yoffset = screen_height/2 - player.rect.y;

pg.init()
screen_width, screen_height = 1280, 720
screen = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption("Oho")
clock = pg.time.Clock()
pg.mouse.set_visible(False)

player = Player()
player_group = pg.sprite.Group()
player_group.add(player)

ball_group = pg.sprite.Group()

wall_group = pg.sprite.Group()
lc.level_construct(wall_group, lc.level0)

calendar = Time()

cursor = Cursor()

camera = Camera()

def collision_check():
	#colisão jogador/parede
	for obj in wall_group:
		if player.rect.colliderect(obj):
			if abs(player.rect.bottom - obj.rect.top) < player.yspeed*2:
				player.rect.bottom = obj.rect.top
			if abs(player.rect.right - obj.rect.left) < player.xspeed*2:
				player.rect.right = obj.rect.left
			if abs(player.rect.left - obj.rect.right) < player.xspeed*2:
				player.rect.left = obj.rect.right
			if abs(player.rect.top - obj.rect.bottom) < player.yspeed*2:
				player.rect.top = obj.rect.bottom
	#colisão bola/parede -> https://www.youtube.com/watch?v=1_H7InPMjaY
	for obj in ball_group:
		for obj2 in wall_group:
			if obj.rect.colliderect(obj2):
				obj.kill()

def draw():
	screen.fill((100,100,100))

	for ball in ball_group:
		screen.blit(ball.image, (ball.rect.x + camera.xoffset, ball.rect.y + camera.yoffset))
	screen.blit(player.image, (screen_width/2, screen_height/2))
	for wall in wall_group:
		screen.blit(wall.image, (wall.rect.x + camera.xoffset, wall.rect.y + camera.yoffset))
	screen.blit(cursor.image, (cursor.rect.x, cursor.rect.y))
	
	pg.display.update()

while True:

	for event in pg.event.get():
		if event.type == pg.QUIT:
			pg.quit()
			sys.exit()
		if event.type == pg.MOUSEBUTTONDOWN:
			player.ball_throw()
	
	keys_pressed = pg.key.get_pressed()

	player_group.update()
	ball_group.update()
	calendar.update()
	cursor.update()
	camera.update()
	draw()
	collision_check()

	#Print Debug
	#print("{:.0f}".format(calendar.cur_time//60))
	#print(calendar.week_day[calendar.day%7])

	clock.tick(60)

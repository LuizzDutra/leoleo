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
		self.cur_time = 0 #Tempo que passou desde a criação do objeto com a classe
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

calendar = Time()

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
	calendar.update()
	draw()

	#Print Debug
	print("{:.0f}".format(calendar.cur_time//60))
	print(calendar.week_day[calendar.day%7])

	clock.tick(60)

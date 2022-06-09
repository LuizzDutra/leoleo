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
		self.use_delay = 0.2
		self.last_use = 0
		self.inv_select = 0
		self.item_list = [Item(), Item(), Item(), Item()]
		self.energy = 100
		self.hp = 100

	def ball_throw(self):
		ball_group.add(Ball(self.rect.center))

	def interact(self):
		for door in door_group:
			if abs(self.rect.x - door.rect.center[0]) < 100 and abs(player.rect.y - door.rect.center[1]) < 100:
				door.open()
		for item in drop_item_group:
			if abs(self.rect.x - item.rect.center[0]) < 100 and abs(player.rect.y - item.rect.center[1]) < 100:
				item.interact()
	def control(self):
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
			if (time.time() - self.last_use) > self.use_delay:
				self.item_list[self.inv_select].use()
				self.last_use = time.time()

		if keys_pressed[pg.K_g]:
			self.item_list[self.inv_select].drop()

		if keys_pressed[pg.K_e]:
			self.interact()
			

		if keys_pressed[pg.K_1]:
			self.inv_select = 0
		if keys_pressed[pg.K_2]:
			self.inv_select = 1
		if keys_pressed[pg.K_3]:
			self.inv_select = 2
		if keys_pressed[pg.K_4]:
			self.inv_select = 3
		if keys_pressed[pg.K_t]:
			for item in self.item_list:
				if item.id  == 0:
					item.id = 1

	def update(self):
		self.control()
	
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

class Door(pg.sprite.Sprite):
	def __init__(self, x, y, width, height):
		super().__init__()
		self.image = pg.Surface((width, height))
		self.rect = self.image.get_rect(x = x, y = y)
		self.open_time = 0.5
		self.open_delta = 0
	def open(self):
		if time.time() - self.open_delta > self.open_time:
			self.open_delta = time.time()
			self.image = pg.transform.rotate(self.image, 90)
			self.rect = self.image.get_rect(x = self.rect.x, y = self.rect.y)

#Classe de tempo que será usada para calcular o horário e passar os dias
class Time():
	def __init__(self):
		self.timescale = 60 #Escala de tempo em relação à vida real/ padrão = 60
		self.start_time = time.time()
		self.cur_time = 0 #Tempo que passou desde a criaçãoo do objeto com a classe
		self.day = 1 #Use o operador "%" por 7 (ex:day % 7) no index do "week_day" para pegar o dia da semana/ Ex: dado day = 1 -> weekday[day%7] --> "Segunda"
		self.week_day = {0:"Domingo", 1:"Segunda", 2:"Terca", 3:"Quarta", 4:"Quinta", 5:"Sexta", 6:"Sabado"}
		self.day_duration = 34200
		self.font = pg.font.SysFont("Arial", 16 )
		self.min_offset = 30
		self.hour_offset = 7
	def day_pass_check(self):
		if self.cur_time > self.day_duration:
			self.day += 1
			self.start_time = time.time()
	def text_render(self):
		self.image = self.font.render(("{:.0f}:{:.0f}".format(self.hour, self.min)), True, (255,255,0))
	def update(self):
		self.day_pass_check()
		self.cur_time = (time.time() - self.start_time) * self.timescale
		self.min = (self.cur_time//60 + self.min_offset)  % 60
		self.hour = ((self.cur_time//60+ self.min_offset)//60 + self.hour_offset) %24
		self.text_render()

	
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



class Item():
	def __init__(self, id=0):
		self.sprites = []
		self.sprites.append(pg.Surface((0, 0)))
		self.sprites.append(pg.transform.scale(pg.image.load(os.path.join("Assets", "ball.png")), (16,16)))
		self.id = id
		self.name_dict = {0:"none", 1:"ball"}
		self.name = self.name_dict[id]
		self.image = self.sprites[self.id]
		self.rect = self.image.get_rect()

	def drop(self):
		if self.id != 0:
			drop_item_group.add(self.Drop_Item(self.id))
			self.id = 0

	def use(self):
		if self.id == 1:
			player.ball_throw()
			self.id = 0
	def update(self):
		self.image = self.sprites[self.id]
		self.rect = self.image.get_rect()
		self.name = self.name_dict[self.id]

	class Drop_Item(pg.sprite.Sprite):
		def __init__(self, id=0):
			super().__init__()
			self.id = id
			self.image = item.sprites[id]
			self.rect = self.image.get_rect(center = player.rect.center)
		def interact(self):
			for item in player.item_list:
				if item.id == 0:
					item.id = self.id
					self.kill()
					break


class Hud():
	def __init__(self):
		self.sprites = []
		self.sprites.append(pg.image.load(os.path.join("Assets", "inv_slots.png")))
		self.sprites.append(pg.image.load(os.path.join("Assets", "inv_slots_selected.png")))
		self.pos = [self.sprites[0].get_rect(x = 100, y = 650), self.sprites[0].get_rect(x = 174, y = 650), self.sprites[0].get_rect(x =248, y = 650), self.sprites[0].get_rect(x =322, y = 650)]
	def draw_inv(self):
		screen.blit(self.sprites[0], self.pos[0].topleft)
		screen.blit(self.sprites[0], self.pos[1].topleft)
		screen.blit(self.sprites[0], self.pos[2].topleft)
		screen.blit(self.sprites[0], self.pos[3].topleft)

		if player.inv_select == 0:
			screen.blit(self.sprites[1], self.pos[0].topleft)
		if player.inv_select == 1:
			screen.blit(self.sprites[1], self.pos[1].topleft)
		if player.inv_select == 2:
			screen.blit(self.sprites[1], self.pos[2].topleft)
		if player.inv_select == 3:
			screen.blit(self.sprites[1], self.pos[3].topleft)

		i = 0
		for item in player.item_list:
			screen.blit(item.image, (self.pos[i].centerx - item.rect.width/2, self.pos[i].centery - item.rect.height/2))
			i+=1


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

door_group = pg.sprite.Group()
door_group.add(Door(288, -255, 64, 10))

drop_item_group = pg.sprite.Group()

calendar = Time()

cursor = Cursor()

camera = Camera()

hud = Hud()





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
				print(obj)
				obj.kill()
		for obj3 in door_group:
			if obj.rect.colliderect(obj3):
				obj.kill()
	#colisão porta
	for obj in door_group:
		if player.rect.colliderect(obj):
			if abs(player.rect.bottom - obj.rect.top) < player.yspeed*2:
				player.rect.bottom = obj.rect.top
			if abs(player.rect.right - obj.rect.left) < player.xspeed*2:
				player.rect.right = obj.rect.left
			if abs(player.rect.left - obj.rect.right) < player.xspeed*2:
				player.rect.left = obj.rect.right
			if abs(player.rect.top - obj.rect.bottom) < player.yspeed*2:
				player.rect.top = obj.rect.bottom

arial = pg.font.SysFont("Arial", 25)
def draw():
	screen.fill((100,100,100))

	for ball in ball_group:
		screen.blit(ball.image, (ball.rect.x + camera.xoffset, ball.rect.y + camera.yoffset))
	for player in player_group:
		screen.blit(player.image, (screen_width/2, screen_height/2))
	for wall in wall_group:
		screen.blit(wall.image, (wall.rect.x + camera.xoffset, wall.rect.y + camera.yoffset))
	screen.blit(cursor.image, (cursor.rect.x, cursor.rect.y))
	for door in door_group:
		screen.blit(door.image, (door.rect.x + camera.xoffset, door.rect.y + camera.yoffset))
	for item in drop_item_group:
		screen.blit(item.image, (item.rect.x + camera.xoffset, item.rect.y + camera.yoffset))

	a = ""

	for item in player.item_list:
		a += str(item.name+",")

	screen.blit(calendar.image, (10, 10))
	screen.blit(arial.render(str(player.hp), True, (255,0,0)), (1200,25))
	screen.blit(arial.render(str(player.energy), True, (255,0,255)), (1200,55))
	screen.blit(arial.render(("({},{})".format(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1])), True, (0,255,255)), (screen_width/2, 0))

	screen.blit(arial.render(a, True, (0,0,0)), (0,100))
	screen.blit(arial.render(str(player.inv_select+1), True, (0,0,0)), (0,80))
	
	hud.draw_inv()




	pg.display.update()

last_use = 0
use_delay = 0.5

while True:

	keys_pressed = pg.key.get_pressed()

	

	for event in pg.event.get():
		if event.type == pg.QUIT:
			pg.quit()
			sys.exit()
		if keys_pressed[pg.K_ESCAPE]:
			print("hello")
			pg.quit()
			sys.exit()
		
		
	


	player_group.update()
	ball_group.update()
	door_group.update()
	calendar.update()
	cursor.update()
	camera.update()
	for item in player.item_list:
		item.update()
	draw()
	collision_check()


	#Print Debug
	#print("{:.0f}".format(calendar.cur_time//60))
	#print(calendar.week_day[calendar.day%7])

	clock.tick(60)

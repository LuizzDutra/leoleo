import pygame as pg
import sys, time
import lc
from Player import Player
from Item import Item, drop_item_group, ball_group
from Time import Time
from Camera import Camera
from Cursor import Cursor
from Hud import Hud


pg.init()
screen_width, screen_height = 1280, 720
screen = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption("Oho")
clock = pg.time.Clock()
pg.mouse.set_visible(False)

player = Player()
player_group = pg.sprite.Group()
player_group.add(player)
player.item_list = [Item(2), Item(), Item(), Item(), Item()]

wall_group = pg.sprite.Group()
lc.level_construct(wall_group, lc.level0)

door_group = pg.sprite.Group()
door_group.add(lc.Door(288, -255, 64, 10))

calendar = Time()

cursor = Cursor()
camera = Camera(player.rect, screen_width, screen_height)
hud = Hud()

def control():
		player.xvel = 0
		player.yvel = 0
		if keys_pressed[pg.K_a]:
			player.xvel = -player.xspeed
		if keys_pressed[pg.K_d]:
			player.xvel = +player.xspeed
		if keys_pressed[pg.K_w]:
			player.yvel = -player.yspeed
		if keys_pressed[pg.K_s]:
			player.yvel = +player.yspeed
		if keys_pressed[pg.K_LSHIFT]:
			player.xvel *= 0.5
			player.yvel *= 0.5
		player.rect.x += player.xvel
		player.rect.y += player.yvel
		if keys_pressed[pg.K_f]:
			if (time.time() - player.last_use) > player.use_delay:
				player.item_list[player.inv_select].use(player)
				player.last_use = time.time()
		if keys_pressed[pg.K_g]:
			player.item_list[player.inv_select].drop(player.rect.center)
		if keys_pressed[pg.K_e]:
			interact()
		if keys_pressed[pg.K_1]:
			player.inv_select = 0
		if keys_pressed[pg.K_2]:
			player.inv_select = 1
		if keys_pressed[pg.K_3]:
			player.inv_select = 2
		if keys_pressed[pg.K_4]:
			player.inv_select = 3
		if keys_pressed[pg.K_5]:
			player.inv_select = 4
		if keys_pressed[pg.K_t]:
			for item in player.item_list:
				if item.id  == 0:
					item.id = 1

def interact():
		for door in door_group:
			if abs(player.rect.x - door.rect.center[0]) < 100 and abs(player.rect.y - door.rect.center[1]) < 100:
				door.open()
		for item in drop_item_group:
			if abs(player.rect.x - item.rect.center[0]) < 100 and abs(player.rect.y - item.rect.center[1]) < 100:
				item.interact(player.item_list)

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
	
	for door in door_group:
		screen.blit(door.image, (door.rect.x + camera.xoffset, door.rect.y + camera.yoffset))
	for item in drop_item_group:
		screen.blit(item.image, (item.rect.x + camera.xoffset, item.rect.y + camera.yoffset))

	screen.blit(calendar.image, (10, 10))
	screen.blit(arial.render(str(player.hp), True, (255,0,0)), (1200,25))
	screen.blit(arial.render(str(player.energy), True, (255,0,255)), (1200,55))
	screen.blit(arial.render(("({},{})".format(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1])), True, (0,255,255)), (screen_width/2, 0))

	hud.draw_inv(player.item_list, player.inv_select, screen)
	screen.blit(cursor.image, (cursor.rect.x, cursor.rect.y))

	pg.display.update()

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
		
	control()
	player_group.update()
	ball_group.update()
	door_group.update()
	calendar.update()
	cursor.update()
	camera.update(player.rect)
	for item in player.item_list:
		item.update()

	collision_check()
	draw()


	clock.tick(60)

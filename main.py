from numpy import full
import pygame as pg
import sys
import lc
import sons
from Player import Player, drop_item_group
from Item import Item, Pacoca, Paper_Ball, Manguza, ball_group
from Time import Time
from Camera import Camera
from Cursor import Cursor
from Hud import Hud
from sprite_draw import sprite_draw
from collision import collision_check
from time import sleep

pg.init()
screen_width, screen_height = 1280, 720
fullscreen = False
screen = pg.display.set_mode((screen_width, screen_height), vsync = 1)
pg.display.set_caption("Oho")
clock = pg.time.Clock()
pg.mouse.set_visible(False)

player = Player()
player_group = pg.sprite.Group()
player_group.add(player)
player.inv_list = [Manguza(), Pacoca(), None, None, None]

wall_group = pg.sprite.Group()
lc.level_construct(wall_group, lc.level0)

door_group = pg.sprite.Group()
door_group.add(lc.Door(288, -255, 64, 10))

calendar = Time()

cursor = Cursor()
camera = Camera(player.rect, screen_width, screen_height)
hud = Hud()

outline_draw = []

group_draw_list = [player_group, wall_group, door_group, ball_group, drop_item_group]
collision_group_list = [wall_group, door_group]
interactable_group_list = [door_group]

#sons.musica.play(sons.radio_video, 0, 5000)
#sons.musica_fila(sons.musica, sons.atwa)

while True:
	keys_pressed = pg.key.get_pressed()
	
	for event in pg.event.get():
		if event.type == pg.QUIT:
			pg.quit()
			sys.exit()
		if keys_pressed[pg.K_ESCAPE]:
			print("bye")
			pg.quit()
			sys.exit()
		if keys_pressed[pg.K_F11]:
			if fullscreen:
				pg.display.set_mode((screen_width, screen_height), vsync=1)
				fullscreen = False	
			elif fullscreen == False :
				pg.display.set_mode((screen_width, screen_height), pg.FULLSCREEN, vsync=1)
				fullscreen = True
		
	player.control(keys_pressed)
	player_group.update()
	player.get_interactable_list(drop_item_group, interactable_group_list)
	ball_group.update()

	calendar.update()
	cursor.update()
	camera.update(player.rect)

	collision_check(player, collision_group_list, ball_group)

	sprite_draw(screen, camera, group_draw_list, player.interactable_list)
	hud.draw_inv(screen, player.inv_list, player.inv_select)
	hud.draw_ui(screen, player, calendar, cursor)
	pg.display.update()

	#print(player.inv_list)

	clock.tick(60)
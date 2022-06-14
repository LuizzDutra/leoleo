import pygame as pg
import sys
import lc
import sons
import images
from player import Player, drop_item_group
from item import Item, Pacoca, Paper_Ball, Manguza, Key, ball_group
import calendario
from camera import Camera
from cursor import Cursor
from hud import Hud
from sprite_draw import sprite_draw
from collision import collision_check

pg.init()

fullscreen = False
screen = images.screen
pg.display.set_caption("Oho")
clock = pg.time.Clock()
pg.mouse.set_visible(False)

player = Player()
player_group = pg.sprite.Group()
player_group.add(player)
player.inv_list = [Manguza(), Pacoca(), Key(4)]

wall_group = pg.sprite.Group()
lc.level_construct(wall_group, lc.level0)

door_group = pg.sprite.Group()
door_group.add(lc.Door(288, -255, 10, 64, True, 4))

day_time = calendario.Calendario()

cursor = Cursor()
camera = Camera(player.rect, screen)
hud = Hud(screen)

outline_draw = []

group_draw_list = [wall_group, door_group, ball_group, drop_item_group, player_group]
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
				pg.display.set_mode(screen.get_size())
				fullscreen = False	
			elif fullscreen == False :
				pg.display.set_mode(screen.get_size(), pg.FULLSCREEN)
				fullscreen = True
		
	player.control(keys_pressed)
	player_group.update()
	player.get_interactable_list(drop_item_group, interactable_group_list)
	ball_group.update()

	day_time.update()
	cursor.update()
	camera.update(player.rect, screen)

	collision_check(player, collision_group_list, ball_group)

	sprite_draw(screen, camera, group_draw_list, player.interactable_list)
	hud.draw_inv(screen, player.inv_list, player.inv_select)
	hud.draw_ui(screen, player, day_time, cursor)
	pg.display.update()

	#print(player.inv_list)

	clock.tick(60)
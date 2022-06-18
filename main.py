print("Importando módulos")
import pygame as pg
import sys
import groups
import images
import fontes
import lc
from player import Player
import item
import calendario
from camera import Camera
from cursor import Cursor
from hud import Hud
from sprite_draw import sprite_draw
from collision import collision_check
import debug
from time import time
import sons
print("Módulos importados")

pg.init()

fullscreen = False
screen = images.screen
pg.display.set_caption("Oho")
clock = pg.time.Clock()
pg.mouse.set_visible(False)

player = Player()
groups.player_group.add(player)
player.inv_list = [item.Manguza(), item.Pacoca(), item.Key(4), item.Money(50)]


lc.level_construct(lc.level0)
groups.door_group.add(lc.Door(3.5, -4.5, 0.3, 2, True, 4))

day_time = calendario.Calendario()

cursor = Cursor()
camera = Camera(player.rect, screen)
hud = Hud(screen)


group_draw_list = [groups.wall_group, groups.ground_group, groups.door_group, item.ball_group, groups.drop_item_group, groups.player_group]
collision_group_list = [groups.wall_group, groups.door_group]
interactable_group_list = [groups.door_group]

debug_state = False

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
		if keys_pressed[pg.K_F3]:
			debug_state = not debug_state
		if keys_pressed[pg.K_h]:
			obj = item.Item()
			obj.rect.center = player.rect.center
			groups.drop_item_group.add(obj)
		if keys_pressed[pg.K_F1]:
			player.rect.center = (0,0)

		
	player.control(keys_pressed)
	groups.player_group.update()
	player.get_interactable_list(groups.drop_item_group, interactable_group_list)
	item.ball_group.update()

	day_time.update()
	cursor.update()
	camera.update(player.rect, screen)

	collision_check(player, collision_group_list, groups.ball_group)

	sprite_draw(screen, camera, group_draw_list, player.interactable_list)
	hud.draw_inv(screen, player.inv_list, player.inv_select)
	hud.draw_ui(screen, player, day_time, cursor)

	if debug_state:
		debug.activate_debug(screen, clock, player)

	pg.display.update()
	clock.tick(60)
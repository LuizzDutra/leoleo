import pygame as pg
import sys
import lc
from Player import Player
from Item import Item, drop_item_group, ball_group
from Time import Time
from Camera import Camera
from Cursor import Cursor
from Hud import Hud
from sprite_draw import sprite_draw
from collision import collision_check

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

group_draw_list = [player_group, wall_group, door_group, ball_group, drop_item_group]

collision_group_list = [wall_group, door_group]

interactable_group_list = [door_group, drop_item_group]

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
		
	player.control(keys_pressed)
	player_group.update(interactable_group_list)

	for item in player.item_list:
		item.update()

	ball_group.update()
	calendar.update()
	cursor.update()
	camera.update(player.rect)

	collision_check(player, collision_group_list, ball_group)
	sprite_draw(screen, camera, group_draw_list)
	hud.draw_inv(screen, player.item_list, player.inv_select)
	hud.draw_ui(screen, player, calendar, cursor)

	pg.display.update()

	clock.tick(60)
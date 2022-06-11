import pygame as pg
import os


class Hud():
	def __init__(self):
		pg.font.init()
		self.arial = pg.font.SysFont("Arial", 25)
		self.inv_sprites = []
		self.inv_sprites.append(pg.image.load(os.path.join("Assets", "inv_slots.png")))
		self.inv_sprites.append(pg.image.load(os.path.join("Assets", "inv_slots_selected.png")))
		self.inv_rect = [self.inv_sprites[0].get_rect(x = 100, y = 650), self.inv_sprites[0].get_rect(x = 174, y = 650), self.inv_sprites[0].get_rect(x =248, y = 650), self.inv_sprites[0].get_rect(x =322, y = 650), self.inv_sprites[0].get_rect(x =322+74, y = 650)]
	def draw_inv(self, screen, item_list, inv_select):
		for rect in self.inv_rect:
			screen.blit(self.inv_sprites[0], rect.topleft)

		screen.blit(self.inv_sprites[1], self.inv_rect[inv_select].topleft)
		
		i = 0
		for item in item_list:
			screen.blit(item.image, (self.inv_rect[i].centerx - item.rect.width/2, self.inv_rect[i].centery - item.rect.height/2))
			i+=1
	def draw_ui(self, screen, player, calendar, cursor):
		screen.blit(calendar.image, (10, 10))
		screen.blit(self.arial.render(str(player.hp), True, (255,0,0)), (1200,25))
		screen.blit(self.arial.render(str(player.energy), True, (255,0,255)), (1200,55))
		screen.blit(self.arial.render(("({},{})".format(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1])), True, (0,255,255)), (1280/2, 0))
		screen.blit(cursor.image, (cursor.rect.x, cursor.rect.y))
import pygame as pg
import os

class Hud():
	def __init__(self):
		self.sprites = []
		self.sprites.append(pg.image.load(os.path.join("Assets", "inv_slots.png")))
		self.sprites.append(pg.image.load(os.path.join("Assets", "inv_slots_selected.png")))
		self.pos = [self.sprites[0].get_rect(x = 100, y = 650), self.sprites[0].get_rect(x = 174, y = 650), self.sprites[0].get_rect(x =248, y = 650), self.sprites[0].get_rect(x =322, y = 650), self.sprites[0].get_rect(x =322+74, y = 650)]
	def draw_inv(self, item_list, inv_select, screen):
		for pos in self.pos:
			screen.blit(self.sprites[0], pos.topleft)

		screen.blit(self.sprites[1], self.pos[inv_select].topleft)
		
		i = 0
		for item in item_list:
			screen.blit(item.image, (self.pos[i].centerx - item.rect.width/2, self.pos[i].centery - item.rect.height/2))
			i+=1
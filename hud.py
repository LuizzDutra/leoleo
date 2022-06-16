import pygame as pg
import images
import fontes


class Hud():
	def __init__(self, screen:pg.display.set_mode):
		self.inv_sprites = []
		self.inv_sprites.append(images.inv_select)
		self.inv_sprites.append(images.inv_slot_selected)
		self.inv_rect = [self.inv_sprites[0].get_rect(x = 100, y = 650), self.inv_sprites[0].get_rect(x = 174, y = 650), self.inv_sprites[0].get_rect(x =248, y = 650), self.inv_sprites[0].get_rect(x =322, y = 650), self.inv_sprites[0].get_rect(x =322+74, y = 650)]
	def draw_inv(self, screen, item_list, inv_select):
		for rect in self.inv_rect:
			screen.blit(self.inv_sprites[0], rect.topleft)

		screen.blit(self.inv_sprites[1], self.inv_rect[inv_select].topleft)
		
		for i, item in enumerate(item_list):
			if item != None:
				screen.blit(item.image, (self.inv_rect[i].centerx - item.rect.width/2, self.inv_rect[i].centery - item.rect.height/2))
				screen.blit(fontes.smallarial.render(str(item.name), True, (255,255,255), (127,127,127)), (self.inv_rect[i].x, self.inv_rect[i].y))

	def draw_ui(self, screen:pg.display.set_mode, player, calendar, cursor):
		screen.blit(calendar.image, (10, 10))
		screen.blit(fontes.arial.render(str(player.hp), True, (255,0,0)), (1200,25))
		screen.blit(fontes.arial.render(str(player.energy), True, (255,0,255)), (1200,55))
		screen.blit(fontes.arial.render(str(player.money), True, (0, 200, 0)), (screen.get_width()-80, 85))
		screen.blit(cursor.image, (cursor.rect.x, cursor.rect.y))

import pygame as pg
from utils import outline_image

def sprite_draw(screen, camera, group_draw_list = [], interactable_list = []):
	screen.fill((100,100,100))
	for group in group_draw_list:
		for sprite in group:
			screen.blit(sprite.image, (sprite.rect.x + camera.xoffset, sprite.rect.y + camera.yoffset))

	for obj in interactable_list:
		screen.blit(outline_image(obj.image, (255,255,0)), (obj.rect.x + camera.xoffset, obj.rect.y + camera.yoffset))

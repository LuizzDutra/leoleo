import pygame as pg

def sprite_draw(screen, camera, group_draw_list):
	screen.fill((100,100,100))
	for group in group_draw_list:
		for sprite in group:
			screen.blit(sprite.image, (sprite.rect.x + camera.xoffset, sprite.rect.y + camera.yoffset))
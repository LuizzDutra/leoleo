import pygame as pg
import groups
import sons

def collision_check(player:pg.sprite.Sprite, collision_group_list):
	#colisão jogador/parede
	for group in collision_group_list:
		col_dict = pg.sprite.groupcollide(groups.player_group, group, False, False)
		for player in col_dict:
			for obj in col_dict[player]:
				if abs(obj.rect.bottom - player.rect.top) < 10:
					player.ypos = obj.rect.bottom
				if abs(obj.rect.left - player.rect.right) < 10:
					player.xpos = obj.rect.left - player.rect.width
				if abs(obj.rect.right - player.rect.left) < 10:
					player.xpos = obj.rect.right
				if abs(obj.rect.top - player.rect.bottom) < 10:
					player.ypos = obj.rect.top - player.rect.width
					
	#colisão bola/parede -> https://www.youtube.com/watch?v=1_H7InPMjaY
	for group in collision_group_list:
		col_dict2 = pg.sprite.groupcollide(groups.ball_group, group, False, False)
		for ball in col_dict2:
			for obj in col_dict2[ball]:
				ball.bounce(obj.rect)


import pygame as pg
import groups
import sons
from math import ceil

def collision_check(player:pg.sprite.Sprite, collision_group_list):
	#colisão jogador/parede
	for group in collision_group_list:
		col_dict = pg.sprite.groupcollide(groups.player_group, group, False, False)
		for player in col_dict:
			for obj in col_dict[player]:
				if abs(obj.rect.bottom - player.rect.top) < player.yspeed*2:
					player.rect.top = obj.rect.bottom
				if abs(obj.rect.left - player.rect.right) < player.xspeed*2:
					player.rect.right = obj.rect.left
				if abs(obj.rect.right - player.rect.left) < player.xspeed*2:
					player.rect.left = obj.rect.right
				if abs(obj.rect.top - player.rect.bottom) < player.yspeed*2:
					player.rect.bottom = obj.rect.top
					
	#colisão bola/parede -> https://www.youtube.com/watch?v=1_H7InPMjaY
	for group in collision_group_list:
		col_dict2 = pg.sprite.groupcollide(groups.ball_group, group, False, False)
		for ball in col_dict2:
			ball.kill()
			sons.play_far_effect(player.rect, ball.rect, sons.ball_hit)
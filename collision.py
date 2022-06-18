import sons
from math import ceil

def collision_check(player, collision_group_list, ball_group):
	#colisão jogador/parede
	for group in collision_group_list:
		for obj in group:
			if player.rect.colliderect(obj):
				if abs(obj.rect.bottom - player.rect.top) < player.yspeed*2:
					player.rect.y += ceil(abs(player.yvel))
				if abs(obj.rect.left - player.rect.right) < player.xspeed*2:
					player.rect.x -= ceil(abs(player.xvel))
				if abs(obj.rect.right - player.rect.left) < player.xspeed*2:
					player.rect.x += ceil(abs(player.xvel))
				if abs(obj.rect.top - player.rect.bottom) < player.yspeed*2:
					player.rect.y -= ceil(abs(player.yvel))
				
	#colisão bola/parede -> https://www.youtube.com/watch?v=1_H7InPMjaY
	for ball in ball_group:
		for group in collision_group_list:
			for obj in group:
				if ball.rect.colliderect(obj):
					sons.play_far_effect(player.rect, ball.rect, sons.ball_hit)
					ball.kill()
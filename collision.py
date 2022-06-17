import sons

def collision_check(player, collision_group_list, ball_group):
	#colisão jogador/parede
	for group in collision_group_list:
		for obj in group:
			if player.rect.colliderect(obj):
				if abs(player.rect.bottom - obj.rect.top) < player.yspeed*2:
					player.rect.bottom = obj.rect.top
				if abs(player.rect.right - obj.rect.left) < player.xspeed*2:
					player.rect.right = obj.rect.left
				if abs(player.rect.left - obj.rect.right) < player.xspeed*2:
					player.rect.left = obj.rect.right
				if abs(player.rect.top - obj.rect.bottom) < player.yspeed*2:
					player.rect.top = obj.rect.bottom
				
	#colisão bola/parede -> https://www.youtube.com/watch?v=1_H7InPMjaY
	for ball in ball_group:
		for group in collision_group_list:
			for obj in group:
				if ball.rect.colliderect(obj):
					sons.play_far_effect(player.rect, ball.rect, sons.ball_hit)
					ball.kill()
import pygame as pg
import groups

def collision_check(player:pg.sprite.Sprite, collision_group_list):
    #colisão jogador/parede
    for group in collision_group_list:
        col_dict = pg.sprite.groupcollide(groups.player_group, group, False, False)
        for player in col_dict:
            for obj in col_dict[player]:
                if abs(obj.rect.bottom - player.rect.top) < player.yspeed*player.dt+5:
                    player.ypos += abs(player.yvel)*player.dt
                if abs(obj.rect.left - player.rect.right) < player.xspeed*player.dt+5:
                    player.xpos -= abs(player.xvel)*player.dt
                if abs(obj.rect.right - player.rect.left) < player.xspeed*player.dt+5:
                    player.xpos += abs(player.xvel)*player.dt
                if abs(obj.rect.top - player.rect.bottom) < player.yspeed*player.dt+5:
                    player.ypos -= abs(player.yvel)*player.dt
    #colisão bola/parede -> https://www.youtube.com/watch?v=1_H7InPMjaY
    for group in collision_group_list:
        col_dict2 = pg.sprite.groupcollide(groups.ball_group, group, False, False)
        for ball in col_dict2:
            for obj in col_dict2[ball]:
                ball.bounce(obj.rect)


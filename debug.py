import pygame as pg
import fontes
from sprite_draw import get_draw_count
from groups import drop_item_group, door_group

def activate_debug(screen, clock:pg.time.Clock, player:pg.rect):
    screen.blit(fontes.smallarial.render(str("Drawing:"+str(get_draw_count())), True, (255,255,0)), (screen.get_width()/2, screen.get_height()-60))
    screen.blit(fontes.smallarial.render(str("Interactables:"+str(len(drop_item_group)+len(door_group))), True, (255,255,0)), (screen.get_width()/2, screen.get_height()-40))
    screen.blit(fontes.smallarial.render(str("frametime:" + str(clock.get_rawtime())), True, (255,255,0)), (screen.get_width()/2, screen.get_height()-20))
    screen.blit(fontes.arial.render(("({},{})".format(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1])), True, (0,255,255)), (screen.get_width()/2, 0))
    player_pos_string = str((player.rect.centerx, player.rect.centery))
    screen.blit(fontes.arial.render(player_pos_string, True, (0, 255, 0)), (screen.get_width()-len(player_pos_string)*10, screen.get_height()-30)) #10/90
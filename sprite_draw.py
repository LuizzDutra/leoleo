import pygame as pg
import fontes
from utils import outline_image, center_blit
from item import Item

last_draw_quantity = 0

#acha a posição de algum efeito extra na imagem de um sprite
#em caso de mudança de tamanho
def get_center_pos(offpos:tuple, image_size:tuple, effect_size:tuple) -> tuple:
    return (offpos[0] + (image_size[0] - effect_size[0])/2, offpos[1] + (image_size[1] - effect_size[1])/2)

def sprite_draw(screen:pg.Surface, camera, player, group_draw_list = [], interactable_list = []):
    global last_draw_quantity
    screen.fill((50,50,50))
    i = 0
    for group in group_draw_list:
        for sprite in group:
            offpos = (sprite.rect.centerx + camera.xoffset - sprite.image.get_width()/2, sprite.rect.centery + camera.yoffset - sprite.image.get_height()/2)
            if offpos[0]+sprite.rect.width > 0 and offpos[0] < screen.get_width() and offpos[1]+sprite.rect.height > 0 and offpos[1] < screen.get_height():
                i+=1
                screen.blit(sprite.image, offpos)
                #desenha outline se a imagem tiver
                if hasattr(sprite, "outline"):
                    screen.blit(sprite.outline, get_center_pos(offpos, sprite.image.get_size(), sprite.outline.get_size()))
                #desenha o glow se a imagem tiver(serve para dar a impressão de brilho)
                if hasattr(sprite, "glow"):
                    screen.blit(sprite.glow, get_center_pos(offpos, sprite.image.get_size(), sprite.glow.get_size()), special_flags=pg.BLEND_RGB_ADD)
    last_draw_quantity = i

    for obj in interactable_list:
        screen.blit(outline_image(obj.image, (255,255,0)), (obj.rect.x + camera.xoffset, obj.rect.y + camera.yoffset))
        if isinstance(obj, Item):
                    screen.blit(fontes.smallarial.render(str(obj.name), True, (255,255,255)), (obj.rect.x + camera.xoffset, obj.rect.top-18+camera.yoffset))

def get_draw_count():
    return last_draw_quantity

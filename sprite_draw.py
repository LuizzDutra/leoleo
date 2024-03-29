import pygame as pg
import fontes
from utils import outline_image, center_blit
from item import Item
from particles import creator_list

last_draw_quantity = 0

#acha a posição de algum efeito extra na imagem de um sprite
#em caso de mudança de tamanho
def get_center_pos(offpos:tuple, image_size:tuple, effect_size:tuple) -> tuple:
    return (offpos[0] + (image_size[0] - effect_size[0])/2, offpos[1] + (image_size[1] - effect_size[1])/2)

def get_offpos(camera, pos, size):
    return (pos[0] + camera.xoffset - size[0]/2, pos[1] + camera.yoffset - size[1]/2)

def sprite_draw(screen:pg.Surface, camera, player, group_draw_list = [], interactable_list = []):
    global last_draw_quantity
    screen.fill((50,50,50))
    particle_delay_blit = []#usado para blitar em certo ponto de modo tardio
    particle_glow_delay_blit = []#usado para blitar o brilho da partícula depois de tudo, fica melhor visualmente
    i = 0
    for group in group_draw_list:
        for sprite in group:
            particle_delay_blit.clear()
            particle_glow_delay_blit.clear()
            offpos = get_offpos(camera, sprite.rect.center, sprite.image.get_size())
            if offpos[0]+sprite.image.get_width() > 0 and offpos[0] < screen.get_width() and offpos[1]+sprite.image.get_height() > 0 and offpos[1] < screen.get_height():
                i += 1
                #desenha a particula do objeto manuseador de partículas
                if hasattr(sprite, "particleHandler"):
                    sprite.particleHandler.delete()
                    sprite.particleHandler.emit()
                    for particle in sprite.particleHandler.particles:
                        particleOffpos = get_offpos(camera, particle.pos, particle.surf.get_size())
                        #checka se a partícula deve ser renderizada na frente do sprite
                        if not particle.backLayer:
                            particle_delay_blit.append([particle.surf, particleOffpos])#blit tardio
                        #checka se a partícula deve ser renderizada atrás do sprite
                        if particle.backLayer:
                            screen.blit(particle.surf, particleOffpos)
                        if particle.glows:#ve se a partícula brilha
                            particle_glow_delay_blit.append([particle.glow, get_center_pos(particleOffpos, particle.surf.get_size(), particle.glow.get_size())])
                        i += 1
                #desenha o sprite normalmente
                screen.blit(sprite.image, offpos)
                for blitArgument in particle_delay_blit:
                    screen.blit(blitArgument[0], blitArgument[1])

                #desenha outline se o sprite tiver
                if hasattr(sprite, "outline"):
                    screen.blit(sprite.outline, get_center_pos(offpos, sprite.image.get_size(), sprite.outline.get_size()))
                    i += 1
        
                #desenha o glow se a imagem tiver(serve para dar a impressão de brilho)
                if hasattr(sprite, "glow"):
                    screen.blit(sprite.glow, get_center_pos(offpos, sprite.image.get_size(), sprite.glow.get_size()), special_flags=pg.BLEND_RGB_ADD)
                    i += 1
                #desenho tardio do glow
                for blitArgument in particle_glow_delay_blit:
                    screen.blit(blitArgument[0], blitArgument[1], special_flags=pg.BLEND_RGB_ADD)

    for obj in interactable_list:
        screen.blit(outline_image(obj.image, (255,255,0)), (obj.rect.x + camera.xoffset, obj.rect.y + camera.yoffset))
        if isinstance(obj, Item):
            screen.blit(fontes.smallarial.render(str(obj.name), True, (255,255,255)), (obj.rect.x + camera.xoffset, obj.rect.top-18+camera.yoffset))

    for creator in creator_list:
        creator.delete()
        creator.emit()
        for particle in creator.particles:
            particleoffpos = get_offpos(camera, particle.pos, particle.surf.get_size())
            screen.blit(particle.surf, particleoffpos)
            if particle.glows:  # ve se a partícula brilha
                screen.blit(particle.glow, particleoffpos, special_flags=pg.BLEND_RGB_ADD)
            i += 1

    last_draw_quantity = i


def get_draw_count():
    return last_draw_quantity

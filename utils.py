import pygame as pg
from time import time

def outline_image(image, color=(0,0,0) , threshold=127):
    out_image = pg.Surface(image.get_size()).convert_alpha()
    out_image.fill((0,0,0,0))
    image_mask = pg.mask.from_surface(image, threshold)
    for point in image_mask.outline():
        out_image.set_at(point,color)
    return out_image

#Remove/replace from list
def rfl(target, ilist, replace=True, term=None): 
        if replace:
            for i,item in enumerate(ilist):
                if item == target:
                    ilist[i] = term
                    return
        for i,item in enumerate(ilist):
            if item == target:
                del ilist[i]
                return

def clamp(number:float, min:float, max:float) -> float:
    if number < min:
        number = min
    if number > max:
        number = max
    return number

def no_zero(number):
    if number == 0:
        return number+1
    return number

#acha key do dicionario dado um valor
def key_from_value(d:dict, v):
    temp_list = [] #lista temporaria para multiplos achados
    for key,value in d.items():
        if value == v:
            temp_list.append(key)
    if len(temp_list) == 1:
        return temp_list[0]
    elif len(temp_list) == 0:
        return None
    else:
        return temp_list

#key do dicionario por atributo
def key_from_atribute(d:dict, obj, attr:str):
    attr_value = getattr(obj, attr, None)
    if attr_value != None:
        d[attr] = attr_value


#(self.base_surf.get_width()/2 - self., self.base_surf.get_height()/2)
#retorna coordenada para blit onde a imagem blitada fica no centro
def center_blit(surface_size : tuple, image_size : tuple) -> tuple:
    return (surface_size[0]/2 - image_size[0]/2, surface_size[1]/2 - image_size[1]/2)

#essa anijmação tá uma bosta mas é o que tem por hoje
def wobble_sprites(surface:pg.Surface, frames:int, intensity = 1) -> list: #faz uma lista de sprites que balança o a surface passada
    sprites_list = []
    surface.convert_alpha()
    md_surface = surface
    angle_change = (180*intensity)/frames

    for i in range(frames-1):
        if i <= frames/4:
            angle = angle_change * i
        if i >= frames/4:
            angle = angle_change * (frames/4 - (i - frames/4))
        if i >= frames/1.5:
            angle = angle_change * (-frames/4 + (i - frames/1.5))
        #print(angle)
        md_surface = pg.transform.rotate(surface, angle)
        sprites_list.append(md_surface)
    

    return sprites_list

class Animator():
    def __init__(self, sprite_list:list, t:float): #tempo em segundos
        self.sprites = sprite_list
        self.cur_sprite = sprite_list[0]
        self.anim_time = t/len(sprite_list)
        self.anim_last = 0
        self.anim_frame = 0

    def animate(self, modifier = 1) -> pg.Surface:#lógica da animação
        if time() - self.anim_last > self.anim_time * 1/modifier: #o modificador altera a velocidade da animação
                self.anim_last = time()
                self.anim_frame = (self.anim_frame + 1) % len(self.sprites)
                self.cur_sprite = self.sprites[self.anim_frame]
        return self.cur_sprite

    def stop(self):#reseta a animação
        self.anim_frame = 0

def remove_items_left_to_right(t_list:list, quantity:int):
    return t_list[quantity:]
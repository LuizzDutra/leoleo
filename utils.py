import pygame as pg

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
    if len(temp_list) >= 1:
        return temp_list[0]
    else:
        return temp_list

#key do dicionario por atributo
def kfa(d:dict, obj, attr:str):
    attr_value = getattr(obj, attr, None)
    if attr_value != None:
        d[attr] = attr_value
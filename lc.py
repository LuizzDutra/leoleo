import pygame as pg
from time import time
import images
from hud import pop_up
import sons
import groups
from PIL import Image
import os
from random import randint
from utils import outline_image
#Decidi que a escala vai ser 64p:1m
gs = 16 #cada grid tem meio metro
class Wall(pg.sprite.Sprite):
    def __init__(self, pos:tuple, pos2:tuple, id):
        super().__init__()
        self.corner = (pos2[0]*gs+gs, pos2[1]*gs+gs)
        self.width = self.corner[0] - pos[0]*gs
        self.height = self.corner[1] - pos[1]*gs
        self.rect = pg.Rect((pos[0]*gs, pos[1]*gs), (self.width, self.height))
        #imagem em forma de tiles
        self.blit_images = images.wall_list[id]
        self.blit_h_image = self.blit_images[0] #parede horizontal
        self.blit_v_image = pg.transform.rotate(self.blit_images[0], 90) #parede vertical
        self.blit_image_size = self.blit_images[0].get_size()
        self.image = pg.Surface((self.rect.width, self.rect.height))
        if self.width > self.height:
            range_max = int(self.image.get_size()[0]/self.blit_image_size[0])
            for x in range(0, range_max):
                if x == range_max-1 or x == 0:
                    self.image.blit(self.blit_images[1], (x*self.blit_image_size[0], 0))
                else:
                    self.image.blit(self.blit_h_image, (x*self.blit_image_size[0], 0))
        if self.width < self.height:
            range_max = int(self.image.get_size()[1]/self.blit_image_size[1])
            for y in range(0, range_max):
                if y == range_max - 1 or y == 0:
                    self.image.blit(self.blit_images[1], (0, y*self.blit_image_size[1]))
                else:
                    self.image.blit(self.blit_v_image, (0, y*self.blit_image_size[1]))
        else:
            self.image.blit(self.blit_images[1], (0, 0))
        del self.blit_images
        del self.blit_image_size
        del self.width
        del self.height

class Ground(pg.sprite.Sprite):
    def __init__(self, pos:tuple, id, rot=False):
        super().__init__()
        rot_dict = {0:90, 1:180, 2:270, 3:0}
        if rot:
            self.image = pg.transform.rotate(images.ground_list[id], rot_dict[randint(0, 3)])
        else:
            self.image = images.ground_list[id]
        self.rect = self.image.get_rect(topleft = (pos[0]*gs , pos[1]*gs))

class Door(pg.sprite.Sprite):
    def __init__(self, x, y, width, height, locked=False, id = 0, closed = True, mirror = False):
        super().__init__()
        if width > height:
            self.image = pg.transform.scale(images.door, (width*gs, height*gs))
            self.vertical = False
        if width < height:
            self.image = pg.transform.scale(pg.transform.rotate(images.door, (-90)), (width*gs, height*gs))
            self.vertical = True
        if width == height:
            self.image = pg.transform.scale(images.door, (width*gs, height*gs))
            self.vertical = True
        self.mirror = mirror
        self.mirror_factor = 1
        if self.mirror:
            self.image = pg.transform.rotate(self.image, 180)
            self.mirror_factor = -1
        self.rect = self.image.get_rect(x = x*gs, y = y*gs)
        self.open_time = 0.5
        self.open_delta = 0
        self.locked = locked
        self.id = id
        self.closed = closed

    def lock(self):
        if self.closed:
            self.locked = True
            sons.play_far_effect(self.rect, sons.key)
    
    def unlock(self):
        self.locked = False
        sons.play_far_effect(self.rect, sons.key)

    def lock_unlock(self, id):
        if self.id == id or id == 0: #chave de id=0 -> chave mestra
            if self.locked:
                self.unlock()
            elif not self.locked:
                self.lock()
        else:
            if self.closed:
                sons.effect_play(sons.bad_key)
                pop_up.add_pop("Chave errada")
    def open_close(self):
        self.open_delta = time()
        if self.closed:
            if self.vertical:
                self.image = pg.transform.rotate(self.image, 90 * self.mirror_factor)
            if not self.vertical:
                self.image = pg.transform.rotate(self.image, -90 * self.mirror_factor)
            sons.play_far_effect(self.rect, sons.open_dr)
            if self.mirror:
                if self.vertical:
                    self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
                if not self.vertical:
                    self.rect = self.image.get_rect(topright = self.rect.topright)
            if not self.mirror:
                self.rect = self.image.get_rect(topleft = self.rect.topleft)
        if not self.closed:
            if self.vertical:
                self.image = pg.transform.rotate(self.image, -90 * self.mirror_factor)
            if not self.vertical:
                self.image = pg.transform.rotate(self.image, 90 * self.mirror_factor)
            if self.mirror:
                if self.vertical:
                    self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
                if not self.vertical:
                    self.rect = self.image.get_rect(topright = self.rect.topright)
            if not self.mirror:
                self.rect = self.image.get_rect(x = self.rect.x, y = self.rect.y)

            sons.play_far_effect(self.rect, sons.cls_dr)
        self.closed = not self.closed

    def interact(self, rect):
        if time() - self.open_delta > self.open_time:
            if self.locked:
                sons.play_far_effect(self.rect, sons.locked)
                pop_up.add_pop("Trancada")
            if not self.locked:
                self.open_close()

class Level_sprite(pg.sprite.Sprite):
    def __init__(self, image, x=0, y=0):
        super().__init__()
        self.image = pg.Surface((image.size[0]*gs, image.size[1]*gs))
        self.rect = self.image.get_rect(x = x, y = y)
class Level_partition_sprite(pg.sprite.Sprite):
    def __init__(self, image, x=0, y=0):
        super().__init__()
        self.image = image
        self.image.convert()
        self.rect = self.image.get_rect(x = x, y = y)



#função usada para carregar os niveis inicialmente e os recarregar posteriormente
def load_levels():
    try:
        global level0
        level0 = Image.open(os.path.join("Assets", "Levels", "level0.png"), "r")
    except Exception as error:
        level0 = None
        print("Level missing")
load_levels() 

def get_pallete(image:Image.Image) -> list:
    temp_pallete_list = image.getpalette()
    pallete_list = []
    for i in range(0, len(temp_pallete_list), 3):
        pallete_list.append((temp_pallete_list[i], temp_pallete_list[i+1],temp_pallete_list[i+2]))
    return pallete_list

def draw_level(level_image, part_quantity, outline=False):
    level_surface = Level_sprite(level_image)
    level_surface.image.fill((50,50,50))
    for ground in groups.ground_group:
        level_surface.image.blit(ground.image, ground.rect.topleft)
    for wall in groups.wall_group:
        level_surface.image.blit(wall.image, wall.rect.topleft)

    level_width = level_surface.image.get_width()
    level_height = level_surface.image.get_height()
    rcq = int(part_quantity**(1/2)) #quantidades de colunas/linhas no quadrado
    i = 0
    for y in range(0,rcq):
        for x in range(0,rcq):
            temp_surface = pg.Surface((level_width/rcq, level_height/rcq))
            temp_surface.blit(level_surface.image, (-x*(level_width/rcq), -y*(level_height/rcq)))
            if outline:
                temp_surface.blit(outline_image(temp_surface, (255,255,0)), (0,0))
            groups.level_surface_group.add(Level_partition_sprite(temp_surface, x*(level_width/rcq), y*(level_height/rcq)))
            i += 1
    print("Mapa particionado em {}".format(i))

def level_construct(level_image:Image.Image, part_quantity=25):
    print("Carrengando mapa")
    try:
        start = time()
        for surface in groups.level_surface_group:
            surface.kill()
        for wall in groups.wall_group:
            wall.kill()
        for ground in groups.ground_group:
            ground.kill()
        level_size = level_image.size
        pallete = get_pallete(level_image)
        check_list = []
        wide_check = False

        for y in range(0, level_size[1]):
            for x in range(0, level_size[0]):
                if (x,y) not in check_list:
                    color = pallete[level_image.getpixel((x,y))]
                    #paredes horizontais
                    wide_check = False
                    wall_cords = []
                    if color in images.wall_list:
                        if (x-1, y) in check_list:
                            wall_cords.append((x-1, y))
                        else:
                            wall_cords.append((x, y))
                        wall_cords.append((x, y))
                        for i in range(x+1, level_size[0]):
                            if pallete[level_image.getpixel((i, y))] == color:
                                wall_cords[1] = (i, y)
                                check_list.append((i, y))
                                if not wide_check:
                                    check_list.append((x, y))
                                    wide_check = True
                            else:
                                break
                        if (x,y) in check_list:
                            groups.wall_group.add(Wall(wall_cords[0], wall_cords[-1], color))
                    #paredes verticais
                    wide_check = False
                    wall_cords = []
                    if color in images.wall_list:
                        if (x,y) not in check_list:
                            if (x, y-1) in check_list:
                                wall_cords.append((x, y-1))
                            else:
                                wall_cords.append((x,y))
                            wall_cords.append((x,y))
                            for i in range(y+1, level_size[0]):
                                if pallete[level_image.getpixel((x, i))] == color:
                                    wall_cords[1] = (x, i)
                                    check_list.append((x, i))
                                    if not wide_check:
                                        check_list.append((x, y))
                                        wide_check = True
                                else:
                                    break
                            groups.wall_group.add(Wall(wall_cords[0], wall_cords[-1], color))



                    if color in images.ground_list:
                        groups.ground_group.add(Ground((x, y), color))

        draw_level(level0, part_quantity)

        print(len(groups.wall_group.sprites()),"paredes")
        end = time()
        print("Mapa Carregado")
        print(end - start)
    except Exception as error:
        print(error)
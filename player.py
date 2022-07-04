import pygame as pg
import images
from time import time
from item import Item, Paper_Ball
from groups import drop_item_group
from utils import outline_image
from math import degrees, atan2



class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.sprites = []
        self.sprites.append(images.player_image)
        self.image = self.sprites[0]
        self.outline = outline_image(self.image, (255,0,0))
        self.rect = self.image.get_rect(center = (0, 0))
        self.xpos = self.rect.x
        self.ypos = self.rect.y
        self.dt = 0
        self.last = 0
        self.xspeed = 300
        self.yspeed = 300
        self.xvel = 0
        self.yvel = 0
        self.use_delay = 0.2
        self.last_use = 0
        self.inv_select = 0
        self.inv_limit = 5
        self.inv_list = []
        self.energy_max = 100
        self.energy = 100
        self.hp_max = 100
        self.hp = 90
        self.lasthp = self.hp
        self.hit_lasthp = self.hp
        self.lastdmg = 0
        self.money = 0
        self.dead = False
        self.pickup_range = 48
        self.interactable_list = []
        self.iteration_delay = 50 #milisegundos
        self.iteration_last = 0
    def control(self, keys_pressed, key_binds):
        self.dt = pg.time.get_ticks()/1000 - self.last
        self.last = pg.time.get_ticks()/1000
        self.xvel = 0
        self.yvel = 0
        if keys_pressed[key_binds["w_left"]]:
            self.xvel -= self.xspeed
        if keys_pressed[key_binds["w_right"]]:
            self.xvel += self.xspeed
        if keys_pressed[key_binds["w_foward"]]:
            self.yvel -= self.yspeed
        if keys_pressed[key_binds["w_back"]]:
            self.yvel += self.yspeed
        if keys_pressed[key_binds["slow_walk"]]:
            self.xvel //= 2
            self.yvel //= 2
        self.xvel *= self.dt
        self.yvel *= self.dt
        self.xpos += self.xvel
        self.ypos += self.yvel
        if keys_pressed[key_binds["use"]]:
            if (pg.time.get_ticks()/1000 - self.last_use) > self.use_delay:
                self.use_item(self.inv_list[self.inv_select])
                self.last_use = pg.time.get_ticks()/1000
        if keys_pressed[key_binds["drop"]]:
            self.drop_item(drop_item_group)
        if keys_pressed[key_binds["interact"]]:
            if (pg.time.get_ticks()/1000 - self.last_use) > self.use_delay:
                self.interact()
                self.last_use = pg.time.get_ticks()/1000
        if keys_pressed[key_binds["slot0"]]:
            self.inv_select = 0
        if keys_pressed[key_binds["slot1"]]:
            self.inv_select = 1
        if keys_pressed[key_binds["slot2"]]:
            self.inv_select = 2
        if keys_pressed[key_binds["slot3"]]:
            self.inv_select = 3
        if keys_pressed[key_binds["slot4"]]:
            self.inv_select = 4
    def mouse_control(self, mouse_events, wheel=False):
        if not wheel:
            if mouse_events[0]:#botão esquerdo
                if (pg.time.get_ticks()/1000 - self.last_use) > self.use_delay:
                    self.use_item(self.inv_list[self.inv_select])
                    self.last_use = pg.time.get_ticks()/1000
        if wheel:
            if mouse_events == -1:#mouse pra baixo
                if self.inv_select+1 == self.inv_limit:
                    self.inv_select = 0
                else:
                    self.inv_select += 1
            if mouse_events == 1:#mouse pra cima
                if self.inv_select == 0:
                    self.inv_select = self.inv_limit-1
                else:
                    self.inv_select -= 1

    def get_interactable_list(self, item_group:pg.sprite.Group, interactable_group_list = []):
        self.interactable_list = [] #reset da lista
        #interação do personagem/ for loop usado para filtrar os interagiveis por distância.
        #Objetos no alcançe são colocados em uma lista de interação
        for i in range(10, 0, -1):
            for group in interactable_group_list:
                    for obj in group:
                        if abs(self.rect.centerx - obj.rect.center[0]) < self.pickup_range/i and abs(self.rect.centery - obj.rect.center[1]) < self.pickup_range/i:
                            if len(self.interactable_list) == 0:
                                self.interactable_list.append(obj)
            for item in item_group:
                if abs(self.rect.centerx - item.rect.center[0]) < self.pickup_range/i and abs(self.rect.centery - item.rect.center[1]) < self.pickup_range/i:
                    if len(self.interactable_list) == 0:
                        self.interactable_list.append(item)


    def add_item(self, item:pg.sprite.Sprite):
        if len(self.inv_list) < self.inv_limit:
            item.kill()
            self.inv_list.append(item)
            return
        for i, slot in enumerate(self.inv_list):
            if slot == None:
                item.kill()
                self.inv_list[i] = item
                return
    def drop_item(self, group:pg.sprite.Group):
        if self.inv_list[self.inv_select] != None:
            self.inv_list[self.inv_select].rect.center = self.rect.center
            group.add(self.inv_list[self.inv_select])
            self.inv_list[self.inv_select] = None
    def use_item(self, item:pg.sprite.Sprite):
        if item != None:
            item.use(self)
    def interact(self):
        for obj in self.interactable_list:
            if isinstance(obj, Item):
                self.add_item(obj)
            else:
                #print(type)
                obj.interact(self.rect)
    def dmg_blink(self):
        if pg.time.get_ticks()/1000 - self.lastdmg < 1:
            if (pg.time.get_ticks()/1000-self.lastdmg) // 0.2 % 2 == 0:
                self.outline = outline_image(self.image, (255,0,0))
            else:
                self.outline = outline_image(self.image, (255,255,255))
        else:
            self.outline = pg.Surface((0,0))
            self.lasthp = self.hp
            self.hit_lasthp = self.hp
    def got_hit(self):
        if self.hp < self.hit_lasthp:
            self.lastdmg = pg.time.get_ticks()/1000
            self.hit_lasthp = self.hp
    def update(self, screen_size:tuple, drop_item_group, interactable_group_list):
        if self.energy > self.energy_max:
            self.energy = self.energy_max
        if self.hp > self.hp_max:
            self.hp = self.hp_max
        if self.hp <= 0:
            self.dead = True
        while len(self.inv_list) < self.inv_limit:
            self.inv_list.append(None)
        self.angle = -degrees(atan2(pg.mouse.get_pos()[1] - screen_size[1]/2, pg.mouse.get_pos()[0] - screen_size[0]/2)) - 90
        self.image = pg.transform.rotate(self.sprites[0], self.angle)

        self.rect.x = round(self.xpos)
        self.rect.y = round(self.ypos)
        if pg.time.get_ticks() - self.iteration_last > self.iteration_delay:
            self.iteration_last = pg.time.get_ticks()
            self.get_interactable_list(drop_item_group, interactable_group_list)
        self.got_hit()
        self.dmg_blink()
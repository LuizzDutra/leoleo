from code import interact
import pygame as pg
import images
from time import time
from item import Item, Paper_Ball
from groups import drop_item_group
from utils import Animator, outline_image, center_blit, wobble_sprites
from math import degrees, atan2
import particles



class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.body_sprites = [images.player_image]
        self.body_animator = Animator(wobble_sprites(images.player_image, 60, 0.5), 0.5)

        self.body_hit_sprites = wobble_sprites(images.player_image, 32, 1)
        self.body_hit_animator = Animator(self.body_hit_sprites, 0.4)

        self.foot_sprites = []
        self.foot_sprites.append(images.idle_foot)
        self.foot_sprites.append(images.step1)
        self.foot_sprites.append(images.idle_foot)
        self.foot_sprites.append(images.step2)
        self.foot_animator = Animator(self.foot_sprites, 0.6)
        self.foot_anim_time_modifier = 1
        #limite da virada das pernas para a suavização
        self.leg_turn_degree = 60  #as pernas só podem virar até 180 - x graus
        self.idle_body_sprites = [images.player_image]
        self.idle_body_animator =Animator(self.idle_body_sprites, 0.5)

        self.idle_foot_sprites = [images.idle_foot]
        self.idle_foot_animator = Animator(self.idle_foot_sprites, 0.5)

        self.image = pg.Surface((self.body_sprites[0].get_width()*1.5, self.body_sprites[0].get_height()*1.5)) #esse resize serve para a diagonal caber na surface
        self.image.set_colorkey((0,0,0)) #colorkey para vários layers
        self.cur_foot_sprite = pg.Surface((0,0))
        self.cur_body_sprite = pg.Surface((0,0))

        self.anim_state = {"idle" : False, "hit" : False, "left" : False, "right" : False, "up" : False, "down" : False}

        self.outline = outline_image(self.image, (255,0,0))
        self.angle = 0
        self.foot_angle = 0
        self.rect = pg.Rect((0,0), (32,32))
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
        self.dmg_delay = 0.4
        self.money = 0
        self.dead = False
        self.pickup_range = 48
        self.interactable_list = []
        self.iteration_delay = 50 #milisegundos
        self.iteration_last = 0
        self.particleHandler = particles.Particles_Handler()
        self.footStepsTime = 0.2
        self.footStepsLast = 0
    def control(self, keys_pressed, key_binds):
        self.dt = pg.time.get_ticks()/1000 - self.last
        self.last = pg.time.get_ticks()/1000
        self.xvel = 0
        self.yvel = 0

        #reset dos estados
        self.anim_state["left"] = False
        self.anim_state["right"] = False
        self.anim_state["up"] = False
        self.anim_state["down"] = False
        self.anim_state["idle"] = True
        #kybinds e estados de animação
        if keys_pressed[key_binds["w_left"]] and not keys_pressed[key_binds["w_right"]]:
            self.anim_state["left"] = True
            self.anim_state["idle"] = False
            self.xvel -= self.xspeed
        if keys_pressed[key_binds["w_right"]] and not keys_pressed[key_binds["w_left"]]:
            self.anim_state["right"] = True
            self.anim_state["idle"] = False
            self.xvel += self.xspeed
        if keys_pressed[key_binds["w_foward"]] and not keys_pressed[key_binds["w_back"]]:
            self.anim_state["up"] = True
            self.anim_state["idle"] = False
            self.yvel -= self.yspeed
        if keys_pressed[key_binds["w_back"]] and not keys_pressed[key_binds["w_foward"]]:
            self.anim_state["down"] = True
            self.anim_state["idle"] = False
            self.yvel += self.yspeed

        if keys_pressed[key_binds["slow_walk"]]:
            self.xvel //= 2
            self.yvel //= 2
        self.xpos += self.xvel * self.dt
        self.ypos += self.yvel * self.dt
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
    def mouse_control(self, mouse_events, key_binds ,wheel=False):
        if not wheel:
            if mouse_events[key_binds["left_click"]]:#botão esquerdo
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

    def get_interactable_list(self, interactable_group_list = []):
        self.interactable_list = [] #reset da lista
        #interação do personagem/ for loop usado para filtrar os interagiveis por distância.
        #Objetos no alcançe são colocados em uma lista de interação
        for i in range(10, 0, -1):
            for group in interactable_group_list:
                    for obj in group:
                        if abs(self.rect.centerx - obj.rect.center[0]) < self.pickup_range/i and abs(self.rect.centery - obj.rect.center[1]) < self.pickup_range/i:
                            if len(self.interactable_list) == 0:
                                self.interactable_list.append(obj)
                                return

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
                obj.interact()
            self.interactable_list.remove(obj)
    def dmg_blink(self):
        if (pg.time.get_ticks()/1000-self.lastdmg) // 0.2 % 2 == 0:
            self.outline = outline_image(self.image, (255,0,0))
        else:
            self.outline = outline_image(self.image, (255,255,255))
        
    def got_hit_scripts(self):
        if self.hp < self.hit_lasthp: #identifica se foi atingido
            self.lastdmg = pg.time.get_ticks()/1000
            self.hit_lasthp = self.hp
        if pg.time.get_ticks()/1000 - self.lastdmg < self.dmg_delay:
            self.anim_state["hit"] = True
            self.dmg_blink()
        else:
            self.anim_state["hit"] = False
            self.outline = pg.Surface((0,0))
            self.lasthp = self.hp #variável de dano cumulativo(lasthp - hp), delay definido pela variável dmg_delay
            self.hit_lasthp = self.hp

    def get_anim_state(self):
        #estado horizontal
        pass
        #estado vertical
        pass

    def get_cur_sprite(self):
        #sprite perna
        if not self.anim_state["idle"]:
            self.cur_foot_sprite = self.foot_animator.animate(self.foot_anim_time_modifier)
            if time() - self.footStepsLast > self.footStepsTime:
                self.footStepsLast = time()
                self.particleHandler.add_explosion(self.rect.center, 5, 40, 0.5, 0.5, (255,255,255), glow=False, backLayer=True)

        if self.anim_state["idle"]:
            self.cur_foot_sprite = self.idle_foot_animator.animate(self.foot_anim_time_modifier)
        #sprite do corpo
        if self.anim_state["hit"]:
            self.cur_body_sprite = self.body_hit_animator.animate()
        elif self.anim_state["idle"]:
            self.cur_body_sprite = self.idle_body_animator.animate()
        elif not self.anim_state["idle"]:
            self.cur_body_sprite = self.body_animator.animate(self.foot_anim_time_modifier)


    def animate(self, screen_size):#animação pós processamento
        self.angle = -degrees(atan2(pg.mouse.get_pos()[1] - screen_size[1]/2, pg.mouse.get_pos()[0] - screen_size[0]/2))
        if self.angle < 0: #garante que o ângulo seja positivo
            self.angle += 360 

        #surface da perna
        if self.anim_state["idle"]:
            self.foot_angle = self.angle
        else:
            self.foot_angle = -degrees(atan2(self.yvel, self.xvel)) #ângulo de acordo com a velocidade
            if self.foot_angle < 0: #garante que o ângulo seja positivo
                self.foot_angle += 360 

            if abs(self.foot_angle - self.angle) > 180 - self.leg_turn_degree  and abs(self.foot_angle - self.angle) < 180 + self.leg_turn_degree: #suavização para as pernas não virarem 180 para trás
                self.foot_angle -= 180
                self.foot_anim_time_modifier = 0.5
            else:
                self.foot_anim_time_modifier = 1

        #surface da perna
        self.leg_surf = pg.transform.rotate(self.cur_foot_sprite, self.foot_angle)

        #surface do corpo
        self.body_surf = pg.transform.rotate(self.cur_body_sprite, self.angle)
        #processando imagem final
        self.image.fill((0,0,0))
        self.image.blit(self.leg_surf, center_blit(self.image.get_size(), self.leg_surf.get_size()))
        self.image.blit(self.body_surf, center_blit(self.image.get_size(), self.body_surf.get_size()))

    def update(self, screen_size:tuple, interactable_group_list):
        if self.energy > self.energy_max:
            self.energy = self.energy_max
        if self.hp > self.hp_max:
            self.hp = self.hp_max
        if self.hp <= 0:
            self.dead = True
        while len(self.inv_list) < self.inv_limit:
            self.inv_list.append(None)
        
        self.get_cur_sprite()
        self.get_anim_state()
        self.animate(screen_size)

        self.rect.x = round(self.xpos)
        self.rect.y = round(self.ypos)
        if pg.time.get_ticks() - self.iteration_last > self.iteration_delay:
            self.iteration_last = pg.time.get_ticks()
            self.get_interactable_list(interactable_group_list)
        self.got_hit_scripts()
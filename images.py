import pygame as pg
import os

screen_res = (1280, 720)
caption_str = "Leo Leo"
pg.display.set_caption(caption_str)
pg.display.set_icon(pg.transform.scale(pg.image.load(os.path.join("Assets", "bob.png")), (32, 32)))
screen = pg.display.set_mode(screen_res)

default_colorkey = (0,255,0)

errorimage = pg.Surface((32,32))
errorimage.fill((255,0,255))

sprite_path = os.path.join("Assets", "Images", "Sprites")
player_sprite_path = os.path.join(sprite_path, "Player")
texture_path = os.path.join("Assets", "Images", "Textures")
item_path = os.path.join("Assets", "Images", "Items")
hud_path = os.path.join("Assets", "Images", "Hud")

def image_loader(path, image_name:str, alpha=False) -> pg.Surface:
    try:
        if alpha:
            return pg.image.load(os.path.join(path, image_name)).convert_alpha()

        return pg.image.load(os.path.join(path, image_name)).convert()
    except Exception as error:
        print(error)
        return errorimage

#paleta vai estar aqui e não no mapa
BLACK = (0,0,0) #parede0
RED = (255,0,0) #parede1
GREEN = (0,255,0) #grama
BLUE = (0,0,255) #piso
YELLOW = (255,255,0)
PINK = (255,0,255)
CYAN = (0,255,255)


#Barras de energia e vida
bar_width = 100
bar_height = 10
empty_bar = pg.Surface((bar_width,bar_height))
empty_bar.fill((0,0,0))
health_bar = pg.Surface((bar_width,bar_height))
health_bar.fill((255,0,0))
damage_bar = pg.Surface((bar_width, bar_height))
damage_bar.fill((255,255,255))
energy_bar = pg.Surface((bar_width, bar_height))
energy_bar.fill((255,255,0))


player_image = image_loader(player_sprite_path, "ademar.png")
player_image.set_colorkey((0,0,0))#o preto será a transparência
step1 = image_loader(player_sprite_path, "step1.png", True)
step2 = image_loader(player_sprite_path, "step2.png", True)
idle_foot = image_loader(player_sprite_path, "idle.png", True)
inv_select = image_loader(hud_path, "inv_slots.png")
inv_select.set_colorkey(default_colorkey)
inv_slot_selected = image_loader(hud_path, "inv_slots_selected.png")
inv_slot_selected.set_colorkey(default_colorkey)
cursor = image_loader(hud_path, "cursor.png")
cursor.set_colorkey(default_colorkey)
manguza = image_loader(item_path, "manguza.png")
bola_papel = image_loader(item_path, "ball.png")
bola_papel.set_colorkey(default_colorkey)
bola_papel_projetil =  image_loader(item_path, "ball.png")
bola_papel_projetil.set_colorkey(default_colorkey)

wall = image_loader(texture_path, "wall.png")
wall_beam = image_loader(texture_path, "wall_beam.png")
brick = pg.transform.scale(image_loader(texture_path, "brick.png"), (16,16))
grass =  pg.transform.scale(image_loader(texture_path, "grass.png"), (16,16))
concrete =  pg.transform.scale(image_loader(texture_path, "concrete.png"), (16,16))

wall_list = {BLACK:(wall, wall_beam), RED:(brick, brick)}
ground_list = {GREEN:grass, BLUE:concrete}


door = image_loader(texture_path, "door.png")
chave = pg.transform.scale(image_loader(item_path, "chave.png"), (48,48))
chave.set_colorkey(default_colorkey)
money = image_loader(item_path, "money.png")
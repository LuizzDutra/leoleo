import pygame as pg
import os
from spritesheet import Spritesheet

screen_res = (1280, 720)
caption_str = "Leo Leo"
pg.display.set_caption(caption_str)
screen = pg.display.set_mode(screen_res)

default_colorkey = (0,255,0)

errorimage = pg.Surface((32,32))
errorimage.fill((255,0,255))

sprite_path = os.path.join("Assets", "Images", "Sprites")
player_sprite_path = os.path.join(sprite_path, "Player")
npc_sprite_path = os.path.join(sprite_path, "Npc")
texture_path = os.path.join("Assets", "Images", "Textures")
item_path = os.path.join("Assets", "Images", "Items")
hud_path = os.path.join("Assets", "Images", "Hud")


def image_loader(path, image_name: str, alpha=False, resize: tuple = None, mult_resize: float = None) -> pg.Surface:
    try:
        image = pg.image.load(os.path.join(path, image_name))

        if resize is not None:
            image = pg.transform.scale(image, resize)

        if mult_resize is not None:
            image = pg.transform.scale(image, (image.get_width() * mult_resize, image.get_height() * mult_resize))

        if alpha:
            image = image.convert_alpha()
        else:
            image = image.convert()

        return image
    except Exception as error:
        print(error)
        return errorimage

pg.display.set_icon(image_loader("Assets", "bob.png"))

#paleta vai estar aqui e não no mapa
BLACK = (0,0,0,255) #parede0
RED = (255,0,0,255) #parede1
GREEN = (0,255,0,255) #grama
BLUE = (0,0,255,255) #piso
YELLOW = (255,255,0,255)
PINK = (255,0,255,255)
CYAN = (0,255,255,255)


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
weak_wall = image_loader(texture_path, "weak_wall.png")
weak_wall2 = image_loader(texture_path, "weak_wall2.png")
brick = image_loader(texture_path, "brick.png", resize=(16, 16))
grass = image_loader(texture_path, "grass.png", resize=(16, 16))
concrete = image_loader(texture_path, "concrete.png", resize=(16, 16))
chest = image_loader(texture_path, "chest.png", alpha=True, mult_resize=1.25)

destructible_wall_list = {YELLOW: (weak_wall, weak_wall), CYAN: (weak_wall2, weak_wall2)}
wall_list = {BLACK: (wall, wall_beam), RED: (brick, brick)}
ground_list = {GREEN: grass, BLUE: concrete}
container_dict = {0: chest}


door = image_loader(texture_path, "door.png")
chave = pg.transform.scale(image_loader(item_path, "chave.png"), (48, 48))
chave.set_colorkey(default_colorkey)
money = image_loader(item_path, "money.png")

npc_lista = []
sprite_obj = Spritesheet(os.path.join(npc_sprite_path,"doux.png"))
for num in range(1,5):
    npc_lista.append(sprite_obj.sprite_load(f"sprite_dino_idle_{num}.png",(0,0,0)))
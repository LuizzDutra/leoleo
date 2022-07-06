import pygame as pg
import os

res = [(1280, 720), (1600, 900), (1920, 1080)]
screen_res = res[0]
caption_str = "Leo Leo"
pg.display.set_caption(caption_str)
pg.display.set_icon(pg.transform.scale(pg.image.load(os.path.join("Assets", "Images", "Sprites", "Player", "bob.png")), (32, 32)))
screen = pg.display.set_mode(screen_res)
default_colorkey = (0,255,0)

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


player_image = pg.transform.scale(pg.image.load(os.path.join("Assets", "Images", "Sprites", "Player", "bob.png")), (32, 32)).convert_alpha()
inv_select = pg.image.load(os.path.join("Assets", "Images", "Hud", "inv_slots.png")).convert()
inv_select.set_colorkey(default_colorkey)
inv_slot_selected = pg.image.load(os.path.join("Assets", "Images", "Hud", "inv_slots_selected.png")).convert()
inv_slot_selected.set_colorkey(default_colorkey)
cursor = pg.image.load(os.path.join("Assets", "Images", "Hud", "cursor.png"))
cursor.set_colorkey(default_colorkey)
errorimage = pg.image.load(os.path.join("Assets", "Images", "error.png")).convert()
manguza = pg.Surface((32,32)).convert()
bola_papel = pg.transform.scale(pg.image.load(os.path.join("Assets", "Images", "Items", "ball.png")), (16,16)).convert()
bola_papel.set_colorkey(default_colorkey)
bola_papel_projetil =  pg.transform.scale(pg.image.load(os.path.join("Assets", "Images", "Items", "ball.png")), (16,16)).convert()
bola_papel_projetil.set_colorkey(default_colorkey)
#paleta vai estar aqui e não no mapa
BLACK = (0,0,0) #parede0
RED = (255,0,0) #parede1
GREEN = (0,255,0) #grama
BLUE = (0,0,255) #piso
YELLOW = (255,255,0)
PINK = (255,0,255)
CYAN = (0,255,255)
wall = pg.transform.scale(pg.image.load(os.path.join("Assets", "Images", "Textures", "wall.png")), (16,16)).convert()
wall_beam = pg.transform.scale(pg.image.load(os.path.join("Assets", "Images", "Textures", "wall_beam.png")), (16,16)).convert()
brick = pg.transform.scale(pg.image.load(os.path.join("Assets", "Images", "Textures", "brick.png")), (16,16)).convert()
grass =  pg.transform.scale(pg.image.load(os.path.join("Assets", "Images", "Textures", "grass.png")), (16,16)).convert()
concrete =  pg.transform.scale(pg.image.load(os.path.join("Assets", "Images", "Textures", "concrete.png")), (16,16)).convert()

wall_list = {BLACK:(wall, wall_beam), RED:(brick, brick)}
ground_list = {GREEN:grass, BLUE:concrete}


door = pg.image.load(os.path.join("Assets", "Images", "Textures", "door.png")).convert()
chave = pg.transform.scale(pg.image.load(os.path.join("Assets", "Images", "Items", "chave.png")), (48,48)).convert()
chave.set_colorkey(default_colorkey)
money = pg.image.load(os.path.join("Assets", "Images", "Items", "money.png")).convert()
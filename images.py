import pygame as pg
import os

res = [(1280, 720), (1600, 900), (1920, 1080)]
screen_res = res[0]
caption_str = "Leo Leo"
pg.display.set_caption(caption_str)
pg.display.set_icon(pg.transform.scale(pg.image.load(os.path.join("Assets", "Images", "Sprites", "Player", "bob.png")), (32, 32)))
screen = pg.display.set_mode(screen_res)

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


player_image = pg.transform.scale(pg.image.load(os.path.join("Assets", "Images", "Sprites", "Player", "bob.png")), (32, 32)).convert()
inv_select = pg.image.load(os.path.join("Assets", "Images", "Hud", "inv_slots.png")).convert()
inv_slot_selected = pg.image.load(os.path.join("Assets", "Images", "Hud", "inv_slots_selected.png")).convert()
cursor = pg.image.load(os.path.join("Assets", "Images", "Hud", "cursor.png")).convert_alpha()
errorimage = pg.image.load(os.path.join("Assets", "Images", "error.png")).convert()
manguza = pg.Surface((32,32)).convert()
bola_papel = pg.transform.scale(pg.image.load(os.path.join("Assets", "Images", "Items", "ball.png")), (16,16)).convert_alpha()
bola_papel_projetil =  pg.transform.scale(pg.image.load(os.path.join("Assets", "Images", "Items", "ball.png")), (16,16)).convert_alpha()
wall = pg.transform.scale(pg.image.load(os.path.join("Assets", "Images", "Textures", "wall.png")), (32,32)).convert()
brick = pg.transform.scale(pg.image.load(os.path.join("Assets", "Images", "Textures", "brick.png")), (32,32)).convert()
grass =  pg.transform.scale(pg.image.load(os.path.join("Assets", "Images", "Textures", "grass.png")), (32,32)).convert()
concrete =  pg.transform.scale(pg.image.load(os.path.join("Assets", "Images", "Textures", "concrete.png")), (32,32)).convert()
wall_list = [wall, brick]
ground_list = [grass, concrete]
door = pg.image.load(os.path.join("Assets", "Images", "Textures", "door.png")).convert()
chave = pg.transform.scale(pg.image.load(os.path.join("Assets", "Images", "Items", "chave.png")), (48,48)).convert_alpha()
money = pg.image.load(os.path.join("Assets", "Images", "Items", "money.png")).convert()
import pygame as pg
import os

screen_width, screen_height = 1280, 720
screen = pg.display.set_mode((screen_width, screen_height))

player_image = pg.transform.scale(pg.image.load(os.path.join("Assets", "bob.png")), (32, 32)).convert()
inv_select = pg.image.load(os.path.join("Assets", "inv_slots.png")).convert()
inv_slot_selected = pg.image.load(os.path.join("Assets", "inv_slots_selected.png")).convert()
errorimage = pg.image.load(os.path.join("Assets", "error.png")).convert()
manguza = pg.Surface((32,32)).convert()
bola_papel = pg.transform.scale(pg.image.load(os.path.join("Assets", "ball.png")), (32,32)).convert_alpha()
bola_papel_projetil =  pg.transform.scale(pg.image.load(os.path.join("Assets", "ball.png")), (16,16)).convert_alpha()
wall = pg.transform.scale(pg.image.load(os.path.join("Assets", "wall.png")), (64,64)).convert()
twall_h = pg.transform.scale(wall, (64, 32)).convert()
twall_v = pg.transform.scale(wall, (32, 64)).convert()
chave = pg.transform.scale(pg.image.load(os.path.join("Assets", "chave.png")), (48,48)).convert_alpha()
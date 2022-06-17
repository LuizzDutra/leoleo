import pygame as pg
import os

res = [(1280, 720), (1600, 900), (1920, 1080)]
screen_res = res[0]
screen = pg.display.set_mode(screen_res)

player_image = pg.transform.scale(pg.image.load(os.path.join("Assets", "bob.png")), (32, 32)).convert()
inv_select = pg.image.load(os.path.join("Assets", "inv_slots.png")).convert()
inv_slot_selected = pg.image.load(os.path.join("Assets", "inv_slots_selected.png")).convert()
cursor = pg.image.load(os.path.join("Assets", "cursor.png")).convert_alpha()
errorimage = pg.image.load(os.path.join("Assets", "error.png")).convert()
manguza = pg.Surface((32,32)).convert()
bola_papel = pg.transform.scale(pg.image.load(os.path.join("Assets", "ball.png")), (16,16)).convert_alpha()
bola_papel_projetil =  pg.transform.scale(pg.image.load(os.path.join("Assets", "ball.png")), (16,16)).convert_alpha()
wall = pg.transform.scale(pg.image.load(os.path.join("Assets", "wall.png")), (32,32)).convert()
brick = pg.transform.scale(pg.image.load(os.path.join("Assets", "brick.png")), (32,32)).convert()
grass =  pg.transform.scale(pg.image.load(os.path.join("Assets", "grass.png")), (32,32)).convert()
wall_list = [wall, brick]
ground_list = [grass]
door = pg.image.load(os.path.join("Assets", "door.png")).convert()
chave = pg.transform.scale(pg.image.load(os.path.join("Assets", "chave.png")), (48,48)).convert_alpha()
money = pg.image.load(os.path.join("Assets", "money.png")).convert()
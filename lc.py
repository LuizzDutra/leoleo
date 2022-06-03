import pygame as pg
#Decidi que a escala vai ser 128p:1m
class Wall(pg.sprite.Sprite):
	def __init__(self, width, height, x, y):
		super().__init__()
		self.image = pg.Surface((width, height))
		self.image.fill((30,30,30))
		self.rect = self.image.get_rect(x = x , y = y)

wall0 = Wall(128, 128, 200, 200)

level0 = [wall0]

def level_construct(wall_group, level):
    for wall in wall_group:
        wall.kill()
    for wall in level:
        wall_group.add(wall)
    return wall_group
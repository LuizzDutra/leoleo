import pygame as pg
#Decidi que a escala vai ser 64p:1m

class Wall(pg.sprite.Sprite):
	def __init__(self, x_pos, y_pos, width, height):
		super().__init__()
		self.image = pg.Surface((64*width, 64*height))
		self.image.fill((30,30,30))
		self.rect = self.image.get_rect(x = 64*x_pos , y = -64*y_pos) #na construção o y tem que ser negativo para facilitar na planta



wall0 = Wall(0, 2, 1, 1)
wall1 = Wall(-2, 2, 1, 1)
wall2 = Wall(-1, 5, 1, 1)
wall3 = Wall(1, 5.5*1, 2*1, 1/2)
wall4 = Wall(0, -0.9, 2, 0.1)
wall5 = Wall(3, 4, 0.5, 4)
wall6 = Wall(6.5, 4, 0.5, 4)
wall7 = Wall(3.5, 0.5, 3, 0.5 )
wall8 = Wall(3.5, 4, 1, 0.5)
wall9 = Wall(5.5, 4, 1, 0.5)


level0 = [wall0, wall1, wall2, wall3, wall4, wall5, wall6, wall7, wall8, wall9]

def level_construct(wall_group, level):
    for wall in wall_group:
        wall.kill()
    for wall in level:
        wall_group.add(wall)
    return wall_group
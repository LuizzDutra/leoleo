import pygame as pg
#Decidi que a escala vai ser 64p:1m

class Wall(pg.sprite.Sprite):
	def __init__(self, pos, pos2): #recebe o ponto superior esquerdo e inferior direito de um retângulo
		super().__init__()
		self.gs = 64
		self.image = pg.Surface((abs(self.gs*(pos[0] - pos2[0])), abs(self.gs*(pos[1] - pos2[1]))))
		self.image.fill((30,30,30))
		self.rect = self.image.get_rect(x = self.gs*pos[0] , y = -self.gs*pos[1]) #na construção o y tem que ser negativo para facilitar na planta
	


wall0 = Wall((0, 2), (-1, 1))
wall1 = Wall((-2, 2), (-1, 1))
wall2 = Wall((-1, 5), (0, 4))
wall3 = Wall((1, 5.5), (3, 5))
wall4 = Wall((0, -0.9), (2, -1))
wall5 = Wall((3, 4), (3.5, 0))
wall6 = Wall((6.5, 4), (7, 0))
wall7 = Wall((3.5, 0.5), (6.5, 0))
wall8 = Wall((3.5, 4), (4.5, 3.5))
wall9 = Wall((5.5, 4), (6.5, 3.5))


level0 = [wall0, wall1, wall2, wall3, wall4, wall5, wall6, wall7, wall8, wall9]

def level_construct(wall_group, level):
    for wall in wall_group:
        wall.kill()
    for wall in level:
        wall_group.add(wall)
    return wall_group
import pygame as pg
import os

class Cursor(pg.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.sprites = []
		self.sprites.append(pg.image.load(os.path.join("Assets", "cursor.png")))
		self.image = self.sprites[0]
		self.rect = self.image.get_rect(center = pg.mouse.get_pos())
	def update(self):
		self.rect.center = pg.mouse.get_pos()

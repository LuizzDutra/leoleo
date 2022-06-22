import pygame as pg

class Camera():
	def __init__(self, focus:tuple, screen:pg.display.set_mode):
		self.xoffset = screen.get_width()/2 - focus[0];
		self.yoffset = screen.get_height()/2 - focus[1];
	def update(self, focus:tuple, screen:pg.display.set_mode):
		self.xoffset = screen.get_width()/2 - focus[0];
		self.yoffset = screen.get_height()/2 - focus[1];

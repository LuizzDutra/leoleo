import pygame as pg

class Camera():
	def __init__(self, focus:pg.rect, screen:pg.display.set_mode):
		self.xoffset = screen.get_width()/2 - focus.x;
		self.yoffset = screen.get_height()/2 - focus.y;
	def update(self, focus:pg.rect, screen:pg.display.set_mode):
		self.xoffset = screen.get_width()/2 - focus.x;
		self.yoffset = screen.get_height()/2 - focus.y;
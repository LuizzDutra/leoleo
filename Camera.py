import pygame as pg

class Camera():
	def __init__(self, rect, screen_width, screen_height):
		self.focus = rect
		self.screen_width = screen_width
		self.screen_height = screen_height
		self.xoffset = self.screen_width/2 - self.focus.x;
		self.yoffset = self.screen_height/2 - self.focus.y;
	def update(self, rect):
		self.focus = rect
		self.xoffset = self.screen_width/2 - self.focus.x;
		self.yoffset = self.screen_height/2 - self.focus.y;
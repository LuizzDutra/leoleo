import pygame

class SpriteSheet():
	def __init__(self, image):
		self.sheet = image
		pygame.init()

	def get_image(self, frame, width, height,reverse):

		if reverse == 0:
			image = pygame.Surface((width, height)).convert_alpha()
			image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
			image = pygame.transform.scale(image, (width * 3, height * 3))
			image.set_colorkey((0,0,0))
		
		elif reverse == 1:
			image = pygame.Surface((width, height)).convert_alpha()
			image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
			image = pygame.transform.scale(image, (width * 3, height * 3))
			image = pygame.transform.flip(image,True,False)
			image.set_colorkey((0,0,0))

		return image
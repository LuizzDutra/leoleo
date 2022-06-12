import pygame as pg

def outline_image(image, color=(0,0,0) , threshold=127):
	out_image = pg.Surface(image.get_size()).convert_alpha()
	out_image.fill((0,0,0,0))
	image_mask = pg.mask.from_surface(image, threshold)
	for point in image_mask.outline():
		out_image.set_at(point,color)
	
	return out_image
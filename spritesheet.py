import pygame
import json

class Spritesheet:
    def __init__(self,filename):
        self.filename = filename
        self.spritesheet = pygame.image.load(self.filename)
        self.metadata = self.filename.replace("png","json")
        with open(self.metadata) as file:
            self.data = json.load(file)
        file.close()

    def get_sprite(self,x,y,w,h,reverse):
        
        if reverse == True:
            surf = pygame.Surface((w,h))
            surf.blit(self.spritesheet,(0,0),(x,y,w,h))
            surf = pygame.transform.scale(surf,(w*2.5,h*2.5))
            surf.set_colorkey(((255, 200, 106)))
            surf = pygame.transform.flip(surf,True,False)

        else:
            surf = pygame.Surface((w,h))
            surf.blit(self.spritesheet,(0,0),(x,y,w,h))
            surf = pygame.transform.scale(surf,(w*2.5,h*2.5))
            surf.set_colorkey(((255, 200, 106)))

        return surf

    def sprite_load(self,arq,rev=False):
        dado = self.data["frame"][arq]["p"]
        x,y,w,h = dado["x"],dado["y"],dado["w"],dado["h"]
        imagem = self.get_sprite(x,y,w,h,rev)
        return imagem
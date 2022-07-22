import pygame
from images import npc_lista
from spritesheet import Spritesheet
from dicionarios import dialogo
from utils import Animator

class Npc(pygame.sprite.Sprite):

    def __init__(self,x,y):
        super().__init__()
        self.animation_dino_idle = npc_lista
        self.rect = self.animation_dino_idle[0].get_rect(center=(int(x),int(y)))
        self.falar = dialogo
        self.num_falar = 5
        self.animacao = Animator(self.animation_dino_idle,1.0)
        self.image = self.animation_dino_idle[0]
        '''self.imagem = 0
        self.frame = 0
        self.tempo = 0'''

    def desenhar_dino(self,display):
        display.blit(self.image,self.rect)

    def update(self):
  
        self.animacao_dino() #dt

    def animacao_dino(self): #deltatime

        self.image = self.animacao.animate()

        '''self.tempo += deltatime
        
        if self.tempo > 0.150:
            self.tempo = 0
            self.frame = (self.frame + 1) % len(self.animation_dino_idle)
            self.imagem = self.animation_dino_idle[self.frame]'''
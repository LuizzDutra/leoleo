import pygame
from sprite import SpriteSheet

pygame.init()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.KEY_ESQUERDA = False
        self.KEY_DIREITA = False
        self.CARA_ESQUERDA = False
        self.carregar_frames()
        self.rect = self.movimento_parado_direita[0].get_rect(midbottom=(240,244))
        self.index_frame = 0
        self.tempo_inicial = 0
        self.status = "parado"
        self.imagem = self.movimento_parado_esquerda[0]


    def desenhar(self,tela):
        tela.blit(self.imagem,self.rect)

    def update(self):
        self.velocidade = 0

        if self.KEY_DIREITA: self.velocidade = +2

        elif self.KEY_ESQUERDA: self.velocidade = -2

        self.rect.x += self.velocidade
        self.set_status()
        self.animacao()


    def set_status(self):

        self.status = "parado"

        if self.velocidade < 0: self.status = "movimento_esquerda"

        elif self.velocidade > 0: self.status = "movimento_direita"

    def animacao(self):
        tempo_final = pygame.time.get_ticks()
        
        if self.status == "parado":

            if tempo_final - self.tempo_inicial > 200:
                self.tempo_inicial = tempo_final
                self.index_frame = (self.index_frame + 1) % len(self.movimento_parado_direita)

                if self.CARA_ESQUERDA: self.imagem = self.movimento_parado_esquerda[self.index_frame]
                
                elif not self.CARA_ESQUERDA : self.imagem = self.movimento_parado_direita[self.index_frame]
        else:

            if tempo_final - self.tempo_inicial > 100:
                self.tempo_inicial = tempo_final
                self.index_frame = (self.index_frame + 1) % len(self.movimento_direita)

                if self.status == "movimento_esquerda": self.imagem = self.movimento_esquerda[self.index_frame]
                
                elif self.status == "movimento_direita": self.imagem = self.movimento_direita[self.index_frame]



    def carregar_frames(self):

        imagem = pygame.image.load("doux.png").convert()
        sprite = SpriteSheet(imagem)
        cont = 0

        self.movimento_parado_direita = []
        self.movimento_parado_esquerda = []
        self.movimento_esquerda = []
        self.movimento_direita = []
        for _ in range(4):

            self.movimento_parado_direita.append(sprite.get_image(cont,24,24,0).convert())
            self.movimento_parado_esquerda.append(sprite.get_image(cont,24,24,1).convert())
            cont += 1

        for _ in range(6):

            self.movimento_direita.append(sprite.get_image(cont,24,24,0).convert())
            self.movimento_esquerda.append(sprite.get_image(cont,24,24,1).convert())
            cont += 1
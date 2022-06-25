import pygame
from spritesheet import Spritesheet

class Jogador:
    def __init__(self,x,y):
        self.direita = False
        self.esquerda = False
        self.up = False
        self.down = False
        self.load_sprite()
        self.rect = self.animation_direita[0].get_rect(center=(int(x),int(y)))
        self.vel = 100
        self.velx = 0
        self.vely = 0
        self.state = "idle"
        self.tempo = 0


    def j_desenhar(self,display):

        display.blit(self.imagem,self.rect)

    def animacao(self,delta):

        self.tempo += delta

        if self.state == "idle":
            self.imagem = self.lista_animacao[1]
            return

        if self.state == "movimento_esquerda":
            self.lista_animacao = self.animation_esquerda

        if self.state == "movimento_direita":
            self.lista_animacao = self.animation_direita

        if self.state == "movimento_up":
            self.lista_animacao = self.animation_up
        
        if self.state == "movimento_down":
            self.lista_animacao = self.animation_down

        if self.tempo > 0.150:
            self.tempo = 0
            self.frame = (self.frame + 1) % len(self.lista_animacao)
            self.imagem = self.lista_animacao[self.frame]

    def update(self,dt):

        self.velx = 0
        self.vely = 0

        if self.esquerda and not self.direita:
            self.velx = -self.vel
            self.state = "movimento_esquerda"

        elif self.direita and not self.esquerda:
            self.velx = self.vel
            self.state = "movimento_direita"

        elif self.up and not self.down:
            self.vely = -self.vel
            self.state = "movimento_up"
            

        elif self.down and not self.up:
            self.vely = self.vel
            self.state = "movimento_down"
            
        else:
            self.state = "idle"
            
        self.rect.x += self.velx * dt
        self.rect.y += self.vely * dt
        self.animacao(dt)

    def load_sprite(self):

        sprite = Spritesheet("pokemon.png")
        self.animation_direita = []
        self.animation_esquerda = []
        self.animation_up = []
        self.animation_down = []

        for r in range(1,4):

            self.animation_direita.append(sprite.sprite_load(f"sprite_red_left_{r}.png",rev=True))
            self.animation_esquerda.append(sprite.sprite_load(f"sprite_red_left_{r}.png"))
            self.animation_down.append(sprite.sprite_load(f"sprite_red_down_{r}.png"))
            self.animation_up.append(sprite.sprite_load(f"sprite_red_up_{r}.png"))

        self.frame = 0
        self.imagem = 0
        self.lista_animacao = self.animation_direita
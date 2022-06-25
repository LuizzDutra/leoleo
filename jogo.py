import pygame
import time
from player import Jogador


pygame.init()

class Jogo:
    def __init__(self):
        self.largura,self.altura = 500,400
        self.tela = pygame.display.set_mode((self.largura,self.altura))
        self.jogo_ativo = True
        self.clock = pygame.time.Clock()
        self.tempo_inicial = time.time()
        self.deltatime = 0
        self.jogador = Jogador(250,200)


    def iniciar(self):
        while self.jogo_ativo:
            self.get_delta()
            self.evento()
            self.desenhar()

    def evento(self):

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                self.jogo_ativo = False

            if evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_LEFT:
                    self.jogador.esquerda = True
                if evento.key == pygame.K_RIGHT:
                    self.jogador.direita = True
                if evento.key == pygame.K_UP:
                    self.jogador.up = True
                if evento.key == pygame.K_DOWN:
                    self.jogador.down = True

            if evento.type == pygame.KEYUP:

                if evento.key == pygame.K_LEFT:
                    self.jogador.esquerda = False
                if evento.key == pygame.K_RIGHT:
                    self.jogador.direita = False
                if evento.key == pygame.K_UP:
                    self.jogador.up = False
                if evento.key == pygame.K_DOWN:
                    self.jogador.down = False




    def desenhar(self):

        self.clock.tick(60)
        self.tela.fill("#000000")
        self.jogador.update(self.deltatime)
        self.jogador.j_desenhar(self.tela)
        pygame.display.update()
       

    def get_delta(self):
        tempo_final = time.time()
        self.deltatime = tempo_final - self.tempo_inicial
        self.tempo_inicial = tempo_final



if __name__ == "__main__":
    jogo = Jogo()
    jogo.iniciar()
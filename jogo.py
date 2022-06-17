import pygame
from sys import exit
from player import Player

pygame.init()

largura = 400
altura = 400
tela = pygame.display.set_mode((largura,altura))
bloco_surf = pygame.Surface((largura,altura))
jogador = Player()
clock = pygame.time.Clock()

fonte = pygame.font.Font(None,50)

while True:

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            exit()
        
        if evento.type == pygame.KEYDOWN:

            if evento.key == pygame.K_LEFT:
                jogador.CARA_ESQUERDA = True
                jogador.KEY_ESQUERDA = True

            elif evento.key == pygame.K_RIGHT:
                jogador.CARA_ESQUERDA = False
                jogador.KEY_DIREITA = True

        if evento.type == pygame.KEYUP:

            if evento.key == pygame.K_LEFT:
                jogador.KEY_ESQUERDA = False
            
            elif evento.key == pygame.K_RIGHT:
                jogador.KEY_DIREITA = False

                
    fonte_surface = fonte.render(jogador.status,True,(0,0,0))
    jogador.update()
    bloco_surf.fill((0,0,0))
    tela.blit(bloco_surf,(0,0))
    bloco_surf.blit(fonte_surface,(200,200))
    jogador.desenhar(tela)
    pygame.display.update()
    clock.tick(60)
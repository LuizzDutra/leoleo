import pygame

def debug(info,x,y):
    tela_surface = pygame.display.get_surface()
    fonte = pygame.font.Font(None,50)
    fonte_surface = fonte.render(str(info),True,(255,255,255))
    fonte_rect = fonte_surface.get_rect(topleft=(x,y))
    tela_surface.blit(fonte_surface,fonte_rect)

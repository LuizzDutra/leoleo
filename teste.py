import pygame
import spritesheet
import Debug

pygame.init()

base = 500
altura = 500

BG = (50,50,50)
BLACK = (0,0,0)

tela = pygame.display.set_mode((base,altura))
pygame.display.set_caption("spritesheet")

sprites_sheet_imagem = pygame.image.load("doux.png").convert_alpha()
sprite_sheet = spritesheet.SpriteSheet(sprites_sheet_imagem)

sprite_lista = []
animacao_frames = [4,6,3,4]
animacao = 0
clock = pygame.time.get_ticks()
sprite_cooldown = 75
frame = 0
cont = 0

for animation in animacao_frames:
    lista_temp_sprites = []
    for _ in range(animation):
        lista_temp_sprites.append(sprite_sheet.get_image(cont,24,24,3,BLACK))
        cont += 1
    sprite_lista.append(lista_temp_sprites)


jogo_ativo = True

while jogo_ativo:


    tela.fill(BG)

    
    clock_1 = pygame.time.get_ticks()
    tela.blit(sprite_lista[animacao][frame],(0,0))

    if clock_1 - clock >= sprite_cooldown:
        frame += 1
        clock = clock_1
        if frame >= len(sprite_lista[animacao]):
            frame = 0

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jogo_ativo = False

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                if animacao < len(animacao_frames) - 1:
                    animacao += 1
                    frame = 0
                    print(animacao)
                else:
                    animacao = 0
    
    pygame.display.update()
    pygame.time.Clock().tick(60)
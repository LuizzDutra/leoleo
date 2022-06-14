import pygame as pg
import os

pg.mixer.init()

musica = pg.mixer.Channel(1)

radio_video = pg.mixer.Sound(os.path.join("Assets", "teste.mp3"))
atwa = pg.mixer.Sound(os.path.join("Assets", "ATWA.mp3"))

lista = [atwa, radio_video]

def musica_fila(channel = pg.mixer.Channel, *musicas):
	for musica in musicas:
		channel.queue(musica)
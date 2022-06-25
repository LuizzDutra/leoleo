import pygame as pg
import os

pg.mixer.init(44100)

volume = 1
effect_volume = 0.3

musica = pg.mixer.Channel(0)
def musica_fila(channel = pg.mixer.Channel, *musicas):
	for musica in musicas:
		channel.queue(musica)
pg.mixer.set_reserved(0)

throw = pg.mixer.Sound(os.path.join("Assets", "Sounds", "throw_sound.wav"))
throw.set_volume
ball_hit = pg.mixer.Sound(os.path.join("Assets", "Sounds", "ball_hit.wav"))
cashing = pg.mixer.Sound(os.path.join("Assets", "Sounds", "cashing.mp3"))
key = pg.mixer.Sound(os.path.join("Assets", "Sounds", "unlock.wav"))
locked = pg.mixer.Sound(os.path.join("Assets", "Sounds", "locked.wav"))
open_dr = pg.mixer.Sound(os.path.join("Assets", "Sounds", "open.wav"))
cls_dr = pg.mixer.Sound(os.path.join("Assets", "Sounds", "close.wav"))
bad_key = pg.mixer.Sound(os.path.join("Assets", "Sounds", "bad_key.wav"))

player_center = (0,0)

def effect_play(sound_file:pg.mixer.Sound):
	sound_file.set_volume(effect_volume*volume)
	pg.mixer.find_channel(True).play(sound_file)

def play_far_effect(sound:pg.Rect, sound_file:pg.mixer.Sound, center = player_center):
	distance = ((center[0] - sound.centerx)**2 + (center[1] - sound.centery)**2)**(1/2)
	dis_vol = 1 - distance/1000
	if dis_vol < 0:
		dis_vol = 0
	sound_file.set_volume(dis_vol*effect_volume*volume)
	pg.mixer.find_channel(True).play(sound_file)

def update(center:tuple):
	global player_center
	player_center = center

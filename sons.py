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


sound_path = os.path.join("Assets", "Sounds")

def sound_loader(path, sound_name, volume = 1) -> pg.mixer.Sound:
    try:
        return_sound = pg.mixer.Sound(os.path.join(path, sound_name)) #carrega
        return_sound.set_volume(volume)#muda volume
        return return_sound
    except Exception as error:
        print(error)
        return None

throw = sound_loader(sound_path, "throw_sound.wav")
ball_hit = sound_loader(sound_path, "ball_hit.wav")
cashing = sound_loader(sound_path, "cashing.mp3")
key = sound_loader(sound_path, "unlock.wav")
locked = sound_loader(sound_path, "locked.wav")
open_dr = sound_loader(sound_path, "open.wav")
cls_dr = sound_loader(sound_path, "close.wav")
bad_key = sound_loader(sound_path, "bad_key.wav")
explosion = sound_loader(sound_path, "explosion.wav")

player_center = (0,0)

def effect_play(sound_file:pg.mixer.Sound):
    try:
        sound_file.set_volume(effect_volume*volume)
        pg.mixer.find_channel(True).play(sound_file)
    except:
        print("sound missing")

def play_far_effect(sound:pg.Rect, sound_file:pg.mixer.Sound):
    distance = ((player_center[0] - sound.centerx)**2 + (player_center[1] - sound.centery)**2)**(1/2)
    dis_vol = 1 - distance/1000
    if dis_vol < 0:
        dis_vol = 0
    try:
        sound_file.set_volume(dis_vol*effect_volume*volume)
        pg.mixer.find_channel(True).play(sound_file)
    except:
        print("sound missing")

def update(center:tuple):
    global player_center
    player_center = center

import pygame as pg
import fontes
from time import time

class Calendario():
    def __init__(self):
        self.timescale = 60 #Escala de tempo em relação à vida real/ padrão = 60
        self.start_time = time()
        self.cur_time = 0 #Tempo que passou desde a criaçãoo do objeto com a classe
        self.day = 1 #Use o operador "%" por 7 (ex:day % 7) no index do "week_day" para pegar o dia da semana/ Ex: dado day = 1 -> weekday[day%7] --> "Segunda"
        self.week_day = {0:"Domingo", 1:"Segunda", 2:"Terca", 3:"Quarta", 4:"Quinta", 5:"Sexta", 6:"Sabado"}
        self.day_duration = 34200
        self.font = fontes.smallarial
        self.min_offset = 30
        self.hour_offset = 7
        self.day_end = False
    def day_end_check(self):
        if self.cur_time > self.day_duration:
            self.day_end = True
    def day_advance(self):
        self.day_end = False
        self.day += 1
        self.start_time = time()

    def text_render(self):
        if self.min < 10:
            self.image = self.font.render(("{:.0f}:0{:.0f}".format(self.hour, self.min)), True, (255,255,0))
        else:
            self.image = self.font.render(("{:.0f}:{:.0f}".format(self.hour, self.min)), True, (255,255,0))
    def update(self):
        self.day_end_check()
        self.cur_time = (time() - self.start_time) * self.timescale
        self.min = (self.cur_time//60 + self.min_offset)  % 60
        self.hour = ((self.cur_time//60+ self.min_offset)//60 + self.hour_offset) %24
        self.text_render()

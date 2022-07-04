import pygame as pg
import images
import fontes
from utils import clamp, no_zero

class Hud():
	def __init__(self, screen:pg.display.set_mode):
		self.inv_sprites = []
		self.inv_sprites.append(images.inv_select)
		self.inv_sprites.append(images.inv_slot_selected)
		self.inv_rect = [self.inv_sprites[0].get_rect(x = 100, y = 650), self.inv_sprites[0].get_rect(x = 174, y = 650), self.inv_sprites[0].get_rect(x =248, y = 650), self.inv_sprites[0].get_rect(x =322, y = 650), self.inv_sprites[0].get_rect(x =322+74, y = 650)]
	def draw_inv(self, screen, item_list, inv_select):
		for rect in self.inv_rect:
			screen.blit(self.inv_sprites[0], rect.topleft)

		screen.blit(self.inv_sprites[1], self.inv_rect[inv_select].topleft)
		
		for i, item in enumerate(item_list):
			if item != None:
				screen.blit(item.image, (self.inv_rect[i].centerx - item.rect.width/2, self.inv_rect[i].centery - item.rect.height/2))
				if hasattr(item, "outline"):
					screen.blit(item.outline, (self.inv_rect[i].centerx - item.rect.width/2, self.inv_rect[i].centery - item.rect.height/2))
				screen.blit(fontes.smallarial.render(str(item.name), True, (255,255,255), (127,127,127)), (self.inv_rect[i].x, self.inv_rect[i].y))

	def draw_ui(self, screen:pg.display.set_mode, player, calendar, cursor):
		screen.blit(calendar.image, (10, 10))
		#barra de vida
		screen.blit(images.empty_bar, (screen.get_width()-images.bar_width-20,25))
		screen.blit(pg.transform.scale(images.health_bar, (images.bar_width*clamp((player.hp/player.hp_max), 0, 1), images.bar_height)), (screen.get_width()-images.bar_width-20,25))
		#barra branca que mostra o dano tomado
		screen.blit(pg.transform.scale(images.damage_bar, (images.bar_width*clamp((((player.lasthp-player.hp)/player.hp_max)), 0, 1), images.bar_height)), ((screen.get_width()-images.bar_width)+(clamp(player.hp, 0, player.hp_max)/player.hp_max*images.bar_width)-20,25))
		#barra de energia
		screen.blit(images.empty_bar, (screen.get_width()-images.bar_width-20,55))
		screen.blit(pg.transform.scale(images.energy_bar, (images.bar_width*clamp((player.energy/player.energy_max), 0, 1), images.bar_height)), (screen.get_width()-images.bar_width-20,55))

		screen.blit(fontes.arial.render(str(player.money), True, (0, 200, 0)), (screen.get_width()-80, 85))
		screen.blit(cursor.image, (cursor.rect.x, cursor.rect.y))

class Pop_up():
    def __init__(self, screen:pg.Surface):
        self.screen = screen
        self.pop_queue = []
        self.pop_time = []
        self.popping = False
        self.pop_delay = 1*1000
        self.pop_start = 0
        self.pop_pos = (640,650)
    def add_pop(self, message:str):
        self.pop_queue.append(message)
        self.pop_time.append(pg.time.get_ticks())
    def pop_up(self):
        if not self.popping:
            self.popping = True
        for i, text in enumerate(self.pop_queue):
            if pg.time.get_ticks() - self.pop_time[i] < self.pop_delay:
                blit_image = fontes.arial.render(text, True, (255,255,255), (10,10,10))
                self.screen.blit(blit_image, (self.pop_pos[0] - blit_image.get_width()/2, self.pop_pos[1] - i*25))
            else:
                del self.pop_queue[i]
                del self.pop_time[i]
                self.popping = False
    def update(self):
         if len(self.pop_queue) > 0:
            self.pop_up()
         else:
            self.popping = False
pop_up = Pop_up(images.screen)


class Console():
	def __init__(self):
		self.image = pg.Surface((images.screen.get_width(), images.screen.get_height()/3))
		self.image.fill((0,0,0))
		self.image.set_alpha(200)
		self.user_input = ""
		self.old_user_input = ""
		self.input_list = []
		self.state = False
		self.input = ""
		self.input_select = 0
		self.input_loop = False
		self.str_select = None

	def draw(self, screen:pg.display.set_mode):
		self.arrow_image = fontes.arial.render(">>", True, (255,255,255))
		self.input_image = [fontes.arial.render(self.user_input[:self.str_select], True, (255,255,255)), fontes.arial.render(self.user_input[self.str_select:], True, (255,255,255))]
		self.bar_image = fontes.arial.render("|", True, (255,127,255))
		screen.blit(self.image, (0,0))
		screen.blit(self.arrow_image, (0, self.image.get_height() - 30))
		screen.blit(self.input_image[0], (self.arrow_image.get_width(), self.image.get_height() - 30))
		if self.str_select != None:
			screen.blit(self.input_image[1], (self.arrow_image.get_width() + self.input_image[0].get_width(), self.image.get_height() - 30))
		if pg.time.get_ticks()/1000 // 0.5 % 2 == 0:
			screen.blit(self.bar_image, (self.arrow_image.get_width() + self.input_image[0].get_width(), self.image.get_height()-30))
		for i in range(len(self.input_list)):
			screen.blit(fontes.smallarial.render(str(self.input_list[-i-1]), True, (255,255,255)), (0, self.image.get_height()-100 - 17*i))
	
	def get_input(self):
		for event in self.events:
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_BACKSPACE:
					if len(self.user_input) > 0:
						if self.str_select != None:
							self.user_input = self.user_input[:self.str_select-1] + self.user_input[self.str_select:]
						else:
							self.user_input = self.user_input[:-1]
				elif event.key == pg.K_DOWN:
					if len(self.input_list) > 0:
						if self.input_loop:
							if self.input_select == len(self.input_list)-1:
								self.input_select = 0
							else:
								self.input_select += 1
						else:
							self.input_loop = True
							self.input_select = 0
						self.user_input = self.input_list[self.input_select]
				elif event.key == pg.K_UP:
					if len(self.input_list) > 0:
						if self.input_loop:
							if self.input_select == 0:
								self.input_select = len(self.input_list)-1
							else:
								self.input_select -= 1
						else:
							self.input_loop = True
							self.input_select = len(self.input_list)-1
						self.user_input = self.input_list[self.input_select]
				elif event.key == pg.K_LEFT:
					if self.str_select == None:
						self.str_select = -1
					elif self.str_select > (-1*len(self.user_input)):
						self.str_select -= 1
				elif event.key == pg.K_RIGHT:
					if self.str_select != None and self.str_select < -1:
						self.str_select += 1
					else:
						self.str_select = None
				elif event.key == pg.K_RETURN:
					self.exec_command()
				else:
					if self.str_select == None:
						self.user_input += event.unicode
					else:
						self.user_input = self.user_input[:self.str_select] + event.unicode + self.user_input[self.str_select:]
	def exec_command(self):
		try:
			exec(self.user_input, self.global_dict)
		except Exception as error:
			print(error)
		self.input_list += [self.user_input]
		self.input_select = 0
		self.input_loop = False
		self.user_input = ""
		self.str_select = None
	
	def update(self, screen, state, events, global_dict):
		self.state = state
		if self.state:
			self.global_dict = global_dict
			self.events = events
			self.draw(screen)
			self.get_input()


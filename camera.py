import pygame as pg


class Camera:
    def __init__(self, focus:tuple, screen:pg.display.set_mode):
        self.focus = focus
        #offset de transção
        self.t_xoffset = 0 
        self.t_yoffset = 0
        self.t_xspeed = 0
        self.t_yspeed = 0
        self.t_time = 0.2
        self.t_start = 0
        self.t_transitioning = False
        self.in_transition = False
        self.detransition = False
        self.xoffset = screen.get_width()/2 - self.focus[0]
        self.yoffset = screen.get_height()/2 - self.focus[1]
        self.dt = 0
        self.last = 0
        self.t_point = (0,0)
    def update(self, focus:tuple, screen:pg.display.set_mode):
        self.dt = pg.time.get_ticks()/1000 - self.last
        self.last = pg.time.get_ticks()/1000
        self.focus = focus
        if self.t_transitioning:
            self.t_xoffset += self.t_xspeed*self.dt
            self.t_yoffset += self.t_yspeed*self.dt
            self.xoffset = screen.get_width()/2 - self.st_point[0] + self.t_xoffset
            self.yoffset = screen.get_height()/2 - self.st_point[1] + self.t_yoffset
            if pg.time.get_ticks()/1000 - self.t_start > self.t_time:
                self.t_transitioning = False
                if self.detransition:
                    self.clear_transition()
                if not self.detransition:
                    self.in_transition = True
        elif self.in_transition:
            self.xoffset = screen.get_width()/2 - self.t_point[0]
            self.yoffset = screen.get_height()/2 - self.t_point[1]
        else:
            from config import camera_follow_intensity
            if camera_follow_intensity != 0:
                cam_x_calc = round(((pg.mouse.get_pos()[0] - screen.get_width()/2) / 2) / (1/camera_follow_intensity))
                cam_y_calc = round(((pg.mouse.get_pos()[1] - screen.get_height()/2) / 2) / (1/camera_follow_intensity))
            else:
                cam_x_calc, cam_y_calc = 0, 0
            self.xoffset = (screen.get_width()/2 - self.focus[0]) - cam_x_calc
            self.yoffset = (screen.get_height()/2 - self.focus[1]) - cam_y_calc
        

    #A transição só soma o offset, note a câmera não irá mudar o foco
    #O propósito desta função é ser usadas em cutscenes sem a movimentação do player
    def transition(self, t_point:tuple):
        if self.in_transition:
            self.detransition = True
            self.t_transitioning = True
            self.t_point = t_point
            self.t_xspeed = (t_point[0] - self.focus[0])/self.t_time
            self.t_yspeed = (t_point[1] - self.focus[1])/self.t_time
            self.t_start = pg.time.get_ticks()/1000
        else:
            self.detransition = False
            self.t_transitioning = True
            self.t_point = t_point
            self.st_point = self.focus
            self.t_xspeed = (self.focus[0] - t_point[0])/self.t_time
            self.t_yspeed = (self.focus[1] - t_point[1])/self.t_time
            self.t_start = pg.time.get_ticks()/1000

    def clear_transition(self):
        self.t_transitioning = False
        self.in_transition = False
        self.t_xoffset = 0
        self.t_yoffset = 0
        self.t_xspeed = 0
        self.t_yspeed = 0

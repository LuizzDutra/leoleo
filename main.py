print("Importando módulos")
import pygame as pg
import sys
import groups
import images
import fontes
import lc
from player import Player
import item
import calendario
from camera import Camera
import cursor
from hud import Hud, Console, pop_up
from sprite_draw import sprite_draw
from collision import collision_check
import debug
from time import sleep
import sons
import quests
print("Módulos importados")

pg.init()

fullscreen = False
screen = images.screen
clock = pg.time.Clock()
pg.mouse.set_visible(False)

player = Player()
groups.player_group.add(player)
player.inv_list = [item.Key(4), item.Money(50), item.Manguza(), item.Pacoca()]


lc.level_construct(lc.level0, 25) #cuidado, garanta que a raíz do número de partições divida sem resto a largura e a altura o nível
groups.door_group.add(lc.Door(9, 5, 4, 0.6))
groups.door_group.add(lc.Door(13, 5, 4, 0.6, mirror=True))
groups.door_group.add(lc.Door(8, 10, 0.6, 4, True, 4))
groups.door_group.add(lc.Door(8, 14, 0.6, 4, True, 4, mirror=True))

day_time = calendario.Calendario()


camera = Camera(player.rect, screen)
hud = Hud(screen)
console = Console()
quest_tracker = quests.Quest_tracker()


group_draw_list = [groups.level_surface_group, groups.door_group, item.ball_group, groups.drop_item_group]
collision_group_list = [groups.wall_group, groups.door_group]
interactable_group_list = [groups.drop_item_group, groups.door_group]

key_binds = {"w_foward" : pg.K_w, "w_back" : pg.K_s, "w_left" : pg.K_a, "w_right" : pg.K_d,
            "slow_walk" : pg.K_LSHIFT, "use" : pg.K_f, "interact" : pg.K_e, "drop" : pg.K_g, 
            "slot0" : pg.K_1, "slot1" : pg.K_2, "slot2" : pg.K_3, "slot3" : pg.K_4, "slot4" : pg.K_5}

def evil_spawn():
    obj = item.Item()
    obj.rect.center = player.rect.center
    groups.drop_item_group.add(obj)

console_state = False
debug_state = False
render_delay = 10 #milisegundos
render_last = 0
while True:
    mouse_events = pg.mouse.get_pressed()
    keys_pressed = pg.key.get_pressed()
    scroll_event = (0, True)
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.MOUSEWHEEL:
            scroll_event = (event.y, True)
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                print("bye")
                pg.quit()
                sys.exit()
            if event.key == pg.K_F11:
                pg.display.toggle_fullscreen()
            if event.key == pg.K_F3:
                debug_state = not debug_state
            if event.key == pg.K_F1:
                player.xpos = 0
                player.ypos = 0
            if event.key == pg.K_F2:
                lc.reload_level()
                lc.level_construct(lc.level0)
            if not console_state:
                if event.key == pg.K_l:
                    player.energy = player.energy_max
                    player.hp -= 10
                if event.key == pg.K_j:
                    camera.transition((0,0))
                if event.key == pg.K_h:
                    camera.clear_transition()
                if event.key == pg.K_t:
                    for i, obj in enumerate(player.inv_list):
                        if obj == None:
                            player.inv_list[i] = item.Paper_Ball()
            if event.key == pg.K_F4:
                console_state = not console_state


    if not console_state:
        player.control(keys_pressed, key_binds)
        player.mouse_control(mouse_events)
        player.mouse_control(scroll_event[0], scroll_event[1])
    groups.player_group.update(screen.get_size(), interactable_group_list)
    item.ball_group.update(player.rect)
    sons.update(player.rect.center)

    day_time.update()
    cursor.cursor.update()
    camera.update(player.rect.center, screen)
    collision_check(player, collision_group_list)

    if pg.time.get_ticks() - render_last > render_delay:
        render_last = pg.time.get_ticks()
        sprite_draw(screen, camera, player, group_draw_list, player.interactable_list)
        hud.draw_inv(screen, player.inv_list, player.inv_select)
        hud.draw_ui(screen, player, day_time, cursor.cursor, console.draw)
        pop_up.update()
        if debug_state:
            debug.activate_debug(screen, clock, player)
        pg.display.update()


    console.update(screen, console_state, events, globals())
    quest_tracker.update()




    #pg.display.set_caption(f"{images.caption_str}    {clock.get_fps():.2f}")

    #print(console.user_input)
    sleep(0.001)
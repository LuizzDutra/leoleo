print("Importando módulos")
import pygame as pg
import sys
import groups
import images
import particles
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
from time import sleep, perf_counter
import sons
import quests
import config
from npc import Npc

print("Módulos importados")

pg.init()

fullscreen = False
screen = images.screen
clock = pg.time.Clock()
pg.mouse.set_visible(False)

player = Player()
groups.player_group.add(player)
player.inventory.inv_list = [item.Key(4), item.Money(50), item.Manguza(), item.Pacoca()]

npc = Npc(0,0)
groups.npc_group.add(npc)

lc.load_level("level0")
lc.draw_level(lc.level_loader.levels[0], 25)
groups.door_group.add(lc.Door(9, 5, 4, 0.6))
groups.door_group.add(lc.Door(13, 5, 4, 0.6, mirror=True))
groups.door_group.add(lc.Door(8, 10, 0.6, 4, True, 4))
groups.door_group.add(lc.Door(8, 14, 0.6, 4, True, 4, mirror=True))
groups.container_group.add(lc.Container("baú", (600, 280), 50, 0))

day_time = calendario.Calendario()

camera = Camera(player.rect.center, screen)
hud = Hud(player.inventory.size)
console = Console()
quest_tracker = quests.Quest_tracker()


group_draw_list = [groups.level_surface_group, groups.wall_group, groups.destructible_wall_group, groups.container_group, groups.door_group, groups.npc_group,
                   groups.player_group, groups.ball_group, groups.drop_item_group]

collision_group_list = [groups.wall_group, groups.door_group, groups.container_group, groups.destructible_wall_group]
interactable_group_list = [groups.drop_item_group, groups.door_group, groups.container_group]

def evil_spawn():
    obj = item.Item()
    obj.rect.center = player.rect.center
    groups.drop_item_group.add(obj)

console_state = False
debug_state = False
#config.save(player, day_time) ##debug
config.load_s(player, day_time)
#config.save_cfg() ##debug
config.load_cfg()
start = 0
end = 0
frametime = 0

while True:
    start = perf_counter()
    mouse_events = pg.mouse.get_pressed()
    keys_pressed = pg.key.get_pressed()

    scroll_event = (0, True)
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            config.save(player, day_time)
            config.save_cfg()
            pg.quit()
            sys.exit()
        if event.type == pg.MOUSEWHEEL:
            scroll_event = (event.y, True)
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                config.save(player, day_time)
                config.save_cfg()
                pg.quit()
                sys.exit()
            if event.key == pg.K_F11:
                config.set_res(toggle= True) #fullscreen e janela
            if event.key == pg.K_F3:
                debug_state = not debug_state
            if event.key == pg.K_F1:
                player.xpos = 0
                player.ypos = 0
            if event.key == pg.K_F2:
                lc.level_loader.load_levels()
                lc.construct_load(lc.level_loader.levels[0], "mapaTeste")
            if not console_state:
                if event.key == pg.K_l:
                    player.particleHandler.add_explosion(player.rect.center, 10, 200, 1, 2, (127,60,30),
                                                         glowIntensity=2, vanish=True, circle=True)
                    sons.effect_play(sons.explosion)
                if event.key == pg.K_j:
                    camera.transition((0,0))
                if event.key == pg.K_h:
                    camera.clear_transition()
                if event.key == pg.K_t:
                    for i in range(player.inventory.size):
                        player.inventory.add_item(item.Paper_Ball())
            if event.key == pg.K_F4:
                console_state = not console_state

    if not console_state:
        player.control(keys_pressed, config.key_binds)
        player.mouse_control(mouse_events, config.key_binds)
        player.mouse_control(scroll_event[0], config.key_binds,scroll_event[1])
    groups.player_group.update(screen.get_size(), interactable_group_list)
    item.ball_group.update(player.rect)
    sons.update(player.rect.center)

    day_time.update()
    cursor.cursor.update()
    camera.update(player.rect.center, screen)
    collision_check(player, collision_group_list)

    if pg.time.get_ticks() - config.render_last > config.render_delay:
        config.render_last = pg.time.get_ticks()
        sprite_draw(screen, camera, player, group_draw_list, player.interactable_list)
        hud.draw_inv(screen, player.inventory.get_inv(), player.inv_select)
        hud.draw_ui(screen, player, day_time, cursor.cursor, console.draw)
        pop_up.update()
        npc.update()

        if debug_state:
            debug.activate_debug(screen, player, frametime)
        pg.display.update()

    console.update(screen, console_state, events, globals())
    quest_tracker.update()

    end = perf_counter()
    frametime = (end - start) * 1000


    sleep(0.001)

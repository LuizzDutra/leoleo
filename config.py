#Nesse módulo estará as configurações do jogo e o sistema de save/load
import pygame as pg
import json
from utils import key_from_atribute, key_from_value
import item
import groups
from cryptography.fernet import Fernet

debugger = True #essa variavel serve para guardar o save sem encriptação

#preload das configs default

#configurações de fps
#o fps é dado pela fórmula 1000/render_delay
render_delay = 5 #milisegundos
render_last = 0

#resoluções
res_list = [(1280, 720), (1920, 1080)]
res = res_list[0]
fullscr = False

def set_res(toggle = False):
    global fullscr
    global res
    if toggle:
        fullscr = not fullscr
    if fullscr:
        pg.display.set_mode(res, pg.FULLSCREEN)
    if not fullscr:
        pg.display.set_mode(res)


#teclas e mouse
key_binds = {"w_foward" : pg.K_w, "w_back" : pg.K_s, "w_left" : pg.K_a, "w_right" : pg.K_d,
            "slow_walk" : pg.K_LSHIFT, "use" : pg.K_f, "interact" : pg.K_e, "drop" : pg.K_g, 
            "slot0" : pg.K_1, "slot1" : pg.K_2, "slot2" : pg.K_3, "slot3" : pg.K_4, "slot4" : pg.K_5
            ,"left_click" : 0, "right_click" : 2, "middle_click" : 1}
#cliques do mouse devem seguir o formato do pg.mouse.get_pressed
#0 : botão esquerdo, 1 : botão do meio, 2 : botão direito

#key pra criptografação
e_key = Fernet(b'93bHQ0LCUsjmVKWta8wK2VTJlSQqTR0SeTjDmjk6OUo=')
extension = ".save" #extensão do save
#salva o jogo
def save(player, day_time):
    with open("c_save"+extension, "wb") as f:
        save_dict = {}

        #info do player
        player_dict = {}
        attr_list = ["xpos", "ypos", "hp_max", "hp", "energy_max", "energy", "money"] #lista de atributos a serem mudados
        for i in attr_list:
            key_from_atribute(player_dict, player, i)    #código equivalente -> player_dict["xpos"] = player.xpos
        save_dict["player_data"] = player_dict
        #inv do player
        temp_list = []
        temp_dict = {}
        for i in player.inv_list:
            temp_dict = {}
            if i == None:
                temp_list.append(None)
            elif type(i) == item.Key:
                temp_dict[key_from_value(item.item_dict, type(i))] = i.id
                temp_list.append(temp_dict)
            elif type(i) == item.Money:
                temp_dict[key_from_value(item.item_dict, type(i))] = i.quantity
                temp_list.append(temp_dict)
            else:
                temp_list.append(key_from_value(item.item_dict, type(i)))

        save_dict["inv"] = temp_list

        #informação de dia e hora
        date_dict = {}

        attr_list = ["day", "day_end", "day_duration", "cur_time"]
        for i in attr_list:
            key_from_atribute(date_dict, day_time, i)

        save_dict["date"] = date_dict

        #encripta e salva 
        crypted_save = e_key.encrypt(bytes(json.dumps(save_dict), "utf-8"))
        f.write(crypted_save)

        if debugger:
            with open("save.json", "w") as e:
                json.dump(save_dict, e)

#carrega save
def load_s(player, day_time):
    #descriptografa o save
    try:
        with open("c_save"+extension, "rb") as f:
            crypted_save = f.read()
            save = bytes.decode(e_key.decrypt(crypted_save), "utf-8")
    except:
        print("Não foi possível carregar seu save")
        return
    #tranforma save em json válido
    save_json = json.loads(save)

    #limpando os itens no chão
    groups.drop_item_group.empty()
    groups.ball_group.empty()

    #carregando dados do player
    data = save_json["player_data"]
    for key, value in data.items():
        setattr(player, key, value)

    #carregando inventário do player
    data = save_json["inv"]
    player.inv_list = []
    for i in data:
        if i == None:
            player.inv_list.append(None)
        elif type(i) == dict:
            for key, value in i.items():
                player.inv_list.append(item.item_dict[int(key)](value))
        else:
            player.inv_list.append(item.item_dict[i]())
    
    #carregando data e hora
    data = save_json["date"]
    for key, value in data.items():
        if key == "cur_time":# exceção para atribuir o tempo inicial certo
            day_time.load(value)
        else:
            setattr(day_time, key, value)

    f.close()

#salva configurações
def save_cfg():

    #lista para todas as variáveis de cfg que serão salvas
    save_list = ["key_binds", "render_delay", "res", "fullscr"]

    with open("config.json", "w") as f:
        save_dict = {}

        #dicionario desse módulo para salvar as variáveis
        global_dict = globals()
        for i in save_list:
            try:
                save_dict[i] = global_dict[i]
            except Exception as error:
                print(f"Variável {error} não encontrada para save")

        json.dump(save_dict, f)

#carrega configurações
def load_cfg():
    try:
        with open("config.json", "r") as f:
            config_json = json.load(f)
            
            #dicionario desse módulo para carregar as variáveis
            global_dict = globals()

            #carregando as variaveis
            for key, value in config_json.items():
                if key in global_dict:
                    #exceção das key_binds que evita a falta de teclas associadas
                    if key == "key_binds":
                        for i, j in global_dict[key].items(): 
                            if i not in value:#check de variaveis que não estão presentes no load
                                value[i] = j
                        global_dict[key] = value
                    else:
                        global_dict[key] = value 
                else:
                    print(f"Variável {key} não encontrada para load")
    except Exception as error:
        print(error)
    set_res()

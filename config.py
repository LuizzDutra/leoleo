#Nesse módulo estará as configurações do jogo e o sistema de save/load
import json
from utils import key_from_value, kfa
import item

#salva o jogo
def save(player):
    with open("save.json", "w") as f:
        save_dict = {}

        #info do player
        player_dict = {}
        attr_list = ["xpos", "ypos", "hp_max", "hp", "energy_max", "energy", "money"] #lista de atributos a serem mudados
        for i in attr_list:
            kfa(player_dict, player, i)    #código equivalente -> player_dict["xpos"] = player.xpos

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

        save_dict["player_data"] = player_dict
        json.dump(save_dict, f)

#carrega save
def load_s(player):
    f = open("save.json")
    save_json = json.load(f)

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
        

    f.close()

#salva configurações
def save_cfg():
    #with open("save.json", "w") as f:
    pass

#carrega configurações
def load_cfg():
    #f = open("config.json")
    #config_json = json.load(f)
    #f.close()
    pass
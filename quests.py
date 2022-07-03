import pygame as pg
import item

class Quest():
    def __init__(self):
        self.name = "Unasigned"
        self.time_limit = 0 #em segundos | pode ser None
        self.start = pg.time.get_ticks()/1000
        self.reward = "Unasigned"
        self.completed = False
        self.failed = False
    def check_completion(self):
        pass
    def check_fail(self):
        if self.time_limit != None:
            if pg.time.get_ticks()/1000 - self.start > self.time_limit:
                self.failed = True
    def fail():
        pass #hook pra fazer alguma coisa caso falhe
    def update(self):
        self.check_completion()
        self.check_fail()

class Fetch(Quest): #tipo de quest onde se tem que pegar algum item e entregar pra alguem
    def __init__(self, name, target:item.Quest_Item, time_limit, owner):
        super().__init__()
        self.name = name
        self.time_limit = time_limit
        self.target = target #O item alvo
        self.owner = owner #Pra quem tem que ser entregue
        #O owner seria um npc que teria um inventario
        #Falar com o npc vai ter a opção de dar pra ele o item
        #Como não tem npc ainda eu vou apenas checkar uma lista
    def check_completion(self):
        if self.target in self.owner:
            self.completed = True
    def fail(self):
        self.target.kill()
    def update(self):
        self.check_completion()
        self.check_fail()

class Favor(Quest): #quest onde o npc pede qualquer item daquele tipo/ ex:ele quer uma paçoca, qualquer paçoca serve
    def __init__(self, name, target_type:item.Item, time_limit, owner):
        super().__init__()
        self.name = name
        self.time_limit = time_limit
        self.target_type = target_type
        self.owner = owner
    def check_completion(self):
        for obj in self.owner:
            if isinstance(obj, self.target_type):
                self.completed = True


class Quest_tracker():
    def __init__(self):
        self.started = []
        self.completed = []
        self.failed = []
    def start_quest(self, quest):
        self.started.append(quest)
    def get_quests_name(self):
        print("Started quests:")
        for quest in self.started:
            print(quest.name)
        print("\nCompleted quests:")
        for quest in self.completed:
            print(quest.name)
        print("\nFailed quests:")
        for quest in self.failed:
            print(quest.name)
    def update(self):
        for quest in self.started:
            quest.update()
            if quest.completed == True:
                self.started.remove(quest)
                self.completed.append(quest)
            if quest.failed == True:
                self.started.remove(quest)
                self.failed.append(quest)
                quest.fail()

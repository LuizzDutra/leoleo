import utils


class Inventory:
    def __init__(self, size, type_restriction: list = None, restriction=False):
        self.inv_list: list = []
        self.size = size
        self.typeRestriction = type_restriction  # Apenas esses tipos serão permitidos/nunca serão permitidos
        self.restriction = restriction
        for i in range(self.size):
            self.inv_list.append(None)

    def get_inv(self):
        return self.inv_list

    def current_quantity(self):
        return len(self.inv_list)

    def get_empty_slots(self):
        count = len(self.inv_list)
        for i, j in enumerate(self.inv_list):
            if j is not None:
                count -= 1
        return count

    def add_item(self, target):
        for i, j in enumerate(self.inv_list):
            if j is None:
                if self.typeRestriction is not None:
                    if self.restriction:  # O objeto não pode pertencer ao tipo
                        if j is None and j not in self.typeRestriction:
                            self.inv_list[i] = target
                            return
                    else:  # O objeto tem que pertencer ao tipo
                        if j is None and j in self.typeRestriction:
                            self.inv_list[i] = target
                            return
                else:
                    self.inv_list[i] = target
                    return

    def remove_index(self, index):
        self.inv_list[index] = None

    def remove_item(self, obj):
        utils.rfl(obj, self.inv_list, term=None)

    def clear(self):
        self.inv_list.clear()

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

    def add_item(self, target):
        for i, j in enumerate(self.inv_list):
            if j is None:
                if self.typeRestriction is not None:
                    if self.restriction:  # O objeto não pode pertencer ao tipo
                        if j is None and j not in self.typeRestriction:
                            self.inv_list[i] = target
                    else:  # O objeto tem que pertencer ao tipo
                        if j is None and j in self.typeRestriction:
                            self.inv_list[i] = target
                else:
                    self.inv_list[i] = target

    def remove_item(self, index):
        self.inv_list[index] = None

    def clear(self):
        self.inv_list.clear()

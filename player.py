# player.py
class Player:
    def __init__(self, name):
        self.name = name
        self.current_room = None
        self.inventory = []  # Liste des objets que le joueur possède
    
    def move(self, direction):
        next_room = self.current_room.exits.get(direction)
        if next_room is None:
            print("\nAucune porte dans cette direction !\n")
            return False
        self.current_room = next_room
        print(self.current_room.get_long_description())
        return True

    def take_item(self, item):
        if item in self.current_room.items:
            self.inventory.append(item)
            self.current_room.items.remove(item)
            print(f"\nVous avez pris {item.name}.\n")
            return True
        else:
            print(f"\n{item.name} n'est pas dans cette salle.\n")
            return False

    def drop_item(self, item):
        if item in self.inventory:
            self.inventory.remove(item)
            self.current_room.items.append(item)
            print(f"\nVous avez posé {item.name}.\n")
            return True
        else:
            print(f"\nVous n'avez pas {item.name} dans votre inventaire.\n")
            return False

    def show_inventory(self):
        if self.inventory:
            print("\nVous possédez :")
            for obj in self.inventory:
                print(f"- {obj.name}")
        else:
            print("\nVotre inventaire est vide.")

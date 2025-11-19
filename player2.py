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

    # Prendre un objet
    def take_item(self, item_name):
        item = next((i for i in self.current_room.inventory if i.name.lower() == item_name.lower()), None)
        if item:
            self.inventory.append(item)
            self.current_room.inventory.remove(item)
            print(f"\nVous avez pris {item.name}.\n")
            return True
        else:
            print(f"\nIl n'y a aucun '{item_name}' ici.\n")
            return False

    # Poser un objet
    def drop_item(self, item_name):
        item = next((i for i in self.inventory if i.name.lower() == item_name.lower()), None)
        if item:
            self.inventory.remove(item)
            self.current_room.inventory.append(item)
            print(f"\nVous avez posé {item.name}.\n")
            return True
        else:
            print(f"\nVous n'avez aucun '{item_name}' dans votre inventaire.\n")
            return False

    # Afficher l'inventaire
    def show_inventory(self):
        if self.inventory:
            print("\nVous possédez :")
            for obj in self.inventory:
                print(f"- {obj.name} : {obj.description}")
        else:
            print("\nVotre inventaire est vide.")

import random

class Character:
    """
    Représente un personnage non joueur (PNJ).
    """

    def __init__(self, name, description, current_room, msgs):
        self.name = name
        self.description = description
        self.current_room = current_room
        self.msgs = msgs

    def __str__(self):
        return f"{self.name} : {self.description}"

    def move(self):
        """
        1 chance sur 2 de se déplacer dans une salle adjacente.
        """
        if random.choice([True, False]) is False:
            return False

        possible_rooms = [
            room for room in self.current_room.exits.values()
            if room is not None
        ]

        if not possible_rooms:
            return False

        new_room = random.choice(possible_rooms)

        self.current_room.characters.remove(self)
        new_room.characters.append(self)
        self.current_room = new_room

        return True

    def get_msg(self, player):
        """
        Affiche un message cyclique.
        Le bibliothécaire parle seulement si le joueur a la clé du tiroir.
        """
        if self.name == "bibliothecaire":
            has_key = any(item.name == "cle_tiroir" for item in player.inventory)
            if not has_key:
                print("Le bibliothécaire vous ignore et se tait.")
                return

        if not self.msgs:
            print("Le personnage n’a rien à dire.")
            return

        msg = self.msgs.pop(0)
        print(msg)
        self.msgs.append(msg)
import random
class Character:
    def __init__(self, name, description, current_room, msgs):
        self.name = name
        self.description = description
        self.current_room = current_room
        self.msgs = msgs
        self.can_move = True 

    def move(self):
        # Si le personnage ne peut pas bouger, on arrête  
        if not self.can_move:                             
            return False                                  

        if random.choice([True, False]) is False:
            return False

        possible_rooms = [
            room for room in self.current_room.exits.values()
            if room is not None
        ]

        if not possible_rooms:
            return False

        new_room = random.choice(possible_rooms)

        # retirer de l'ancienne salle
        self.current_room.characters.remove(self)

        # ajouter à la nouvelle
        new_room.characters.append(self)
        self.current_room = new_room

        return True

    def get_msg(self, player):
        # Cas spécial : bibliothécaire
        if self.name == "bibliothecaire":
            has_key = any(item.name == "cle_tiroir" for item in player.inventory)

            if not has_key:
                print("Revenez me voir quand vous saurez ouvrir ce qui est fermé.")
                return

        # Messages cycliques normaux
        if not self.msgs:
            print("Le personnage n’a rien à dire.")
            return

        msg = self.msgs.pop(0)
        print(msg)
        self.msgs.append(msg)

    def __str__(self):
        return f"{self.name} : {self.description}"

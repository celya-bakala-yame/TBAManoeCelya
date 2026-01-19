class Character:
    def __init__(self, name, description, current_room, msgs):
        self.name = name
        self.description = description
        self.current_room = current_room
        self.msgs = msgs

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

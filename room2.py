# room.py
class Room:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.exits = {}
        self.inventory = []        # Liste des objets présents dans la salle
        self.characters = []       # Liste des PNJ présents dans la salle
    

    def get_exit(self, direction):
        return self.exits.get(direction)

    def get_exit_string(self):
        exit_string = "Sorties: "
        for exit, room in self.exits.items():
            if room is not None:
                exit_string += exit + ", "
        return exit_string.strip(", ")

    def get_inventory(self):
        if not self.inventory:
            return "Il n'y a aucun objet ici."
        else:
            return "On voit ici : " + ", ".join([item.name for item in self.inventory])

    def get_long_description(self):
        # Description principale + sorties
        desc = f"\nVous êtes {self.description}\n\n{self.get_exit_string()}\n"
        
        # Objets dans la salle
        if self.inventory:
            desc += f"\n{self.get_inventory()}\n"
        
        # PNJ présents
        if self.characters:
            desc += "\nPersonnages présents :\n"
            for char in self.characters:
                desc += f"- {char.name} : {char.description}\n"
        
        return desc

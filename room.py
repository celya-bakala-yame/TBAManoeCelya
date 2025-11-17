# room.py
class Room:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.exits = {}
        self.items = []        # Liste des objets présents dans la salle
        self.characters = []   # Liste des PNJ présents dans la salle

    def get_exit(self, direction):
        return self.exits.get(direction)

    def get_exit_string(self):
        exit_string = "Sorties: "
        for exit, room in self.exits.items():
            if room is not None:
                exit_string += exit + ", "
        return exit_string.strip(", ")

    def get_long_description(self):
        desc = f"\nVous êtes {self.description}\n\n{self.get_exit_string()}\n"
        
        if self.items:
            desc += "\nObjets dans la salle :\n"
            for item in self.items:
                desc += f"- {item.name} : {item.description}\n"
        
        if self.characters:
            desc += "\nPersonnages présents :\n"
            for char in self.characters:
                desc += f"- {char.name} : {char.description}\n"
        
        return desc

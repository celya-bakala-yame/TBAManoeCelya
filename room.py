# Define the Room class.

class Room:
    """Représente une pièce du jeu."""

    # Define the constructor. 
    def __init__(self, name, description):
        """ Initialise une nouvelle pièce.

        Args:
            name (str): Le nom de la pièce.
            description (str): La description détaillée de la pièce. """

        self.name = name
        self.description = description
        self.exits = {}
    
    # Define the get_exit method.
    def get_exit(self, direction):
        """ Retourne la pièce située dans la direction donnée.

        Args:
            direction (str): La direction souhaitée (ex: "nord", "est").

        Returns:
            Room or None: La pièce correspondant à cette direction,
                          ou None si aucune sortie n'existe. """

        # Return the room in the given direction if it exists.
        if direction in self.exits.keys():
            return self.exits[direction]
        else:
            return None
    
    # Return a string describing the room's exits.
    def get_exit_string(self):
        """ Retourne une chaîne listant toutes les sorties disponibles.

        Returns:
            str: Une phrase du type "Sorties: nord, est"."""

        exit_string = "Sorties: " 
        for exit in self.exits.keys():
            if self.exits.get(exit) is not None:
                exit_string += exit + ", "
        exit_string = exit_string.strip(", ")
        return exit_string

    # Return a long description of this room including exits.
    def get_long_description(self):
        """ Retourne une description complète de la pièce incluant ses sorties.

        Returns:
            str: Une description multilignes de la pièce et de ses sorties."""
            
        return f"\nVous êtes {self.description}\n\n{self.get_exit_string()}\n"
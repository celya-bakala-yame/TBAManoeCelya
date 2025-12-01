# Define the Player class.
class Player():
    """ Représente un joueur dans le jeu.

    Un Player possède :
    - un nom
    - une salle actuelle dans laquelle il se trouve. """

    # Define the constructor.
    def __init__(self, name):
        """ Initialise un nouveau joueur.

        Args:
            name (str): Le nom du joueur."""

        self.name = name
        self.current_room = None
        self.history = []   # <-- historique initialisé vide
    
    # Define the move method.
    def move(self, direction):
        """ Déplace le joueur dans la direction spécifiée si possible.

        Args:
            direction (str): La direction dans laquelle le joueur souhaite se déplacer
                             (ex: "nord", "est", "sud", "ouest").

        Returns:
            bool: True si le déplacement a réussi, False si aucune sortie n'existe
                  dans cette direction.
        
        Prints:
            str: Affiche la description complète de la nouvelle salle ou un message
                 d'erreur si le mouvement est impossible."""
                 
        # Get the next room from the exits dictionary of the current room.
        next_room = self.current_room.exits[direction]

        # If the next room is None, print an error message and return False.
        if next_room is None:
            print("\nAucune porte dans cette direction !\n")
            return False

        
        # Mettre à jour l'historique AVANT le déplacement

        self.history.append(self.current_room)

        # Set the current room to the next room.
        self.current_room = next_room
        print(self.current_room.get_long_description())

        # Affichage automatique de l'historique
        print(self.get_history())

        return True

    def get_history(self):
        """Retourne une chaîne de caractères représentant les pièces visitées."""

        if not self.history:
            return "Vous n'avez encore visité aucune autre pièce."

        lines = ["Vous avez déja visité les pièces suivantes:"]
        for room in self.history:
            # On récupère uniquement la première ligne de la description
            first_line = room.get_long_description().strip().split("\n")[0]
            lines.append("    - " + first_line)

        return "\n".join(lines)

    
# Description: Game class

# Import modules

from room import Room
from player import Player
from command import Command
from actions import Actions

class Game:

    # Constructor
    def __init__(self):
        self.finished = False
        self.rooms = []
        self.commands = {}
        self.player = None
    
    # Setup the game
    def setup(self):

        # Setup commands

        help = Command("help", " : afficher cette aide", Actions.help, 0)
        self.commands["help"] = help
        quit = Command("quit", " : quitter le jeu", Actions.quit, 0)
        self.commands["quit"] = quit
        go = Command("go", " <direction> : se déplacer dans une direction cardinale (N, E, S, O) ou dans les étages (U, D)", Actions.go, 1)
        self.commands["go"] = go
        history = Command("history", " : afficher l'historique des pièces visitées", Actions.history, 0)
        self.commands["history"] = history
        
        # Setup rooms

        hall = Room("Hall", "le hall d'entrée spacieux.")
        self.rooms.append(hall)
        library = Room("Salle de lecture", "une grande bibliothèque calme mais un peu sombre.")
        self.rooms.append(library)
        study1 = Room("Salle de travail 1", "une petite salle silencieuse.")
        self.rooms.append(study1)
        study2 = Room("Salle de travail 2", "une salle avec un étudiant perdu.")
        self.rooms.append(study2)
        study3 = Room("Salle de travail 3", "une salle avec une clé cassée sur une table.")
        self.rooms.append(study3)
        study4 = Room("Salle de travail 4", "une salle calme avec un fantôme mystérieux.")
        self.rooms.append(study4)
        librarian_office = Room("Bureau du bibliothécaire", "le bureau du bibliothécaire, avec un tiroir verrouillé.")
        self.rooms.append(librarian_office)
        secret_corridor = Room("Passage secret", "un couloir caché derrière le bureau.")
        self.rooms.append(secret_corridor)
        archives = Room("Salle des archives", "une pièce silencieuse avec des livres anciens.")
        self.rooms.append(archives)

        # Create exits for rooms

        hall.exits = {"N" : library, "E" : librarian_office, "S" : None, "O" : study4, "U" : None, "D" : None}
        library.exits = {"N" : None, "E" : None, "S" : hall , "O" : study1, "U" : None, "D" : None}
        study1.exits = {"N" : None, "E" : library, "S" : study2, "O" : None, "U" : None, "D" : None}
        study2.exits = {"N" : study1, "E" : None, "S" : study3, "O" : None, "U" : None, "D" : None}
        study3.exits = {"N" : study2, "E" : None, "S" : study4, "O" : None, "U" : None, "D" : None}
        study4.exits = {"N" : study3, "E" : hall, "S" : None, "O" : None, "U" : None, "D" : None}
        librarian_office.exits = {"N" : None, "E" : secret_corridor, "S" : None, "O" : hall, "U" : None, "D" : None}
        secret_corridor.exits = {"N" : None, "E" : None, "S" : None, "O" : librarian_office, "U" : None, "D" : archives}
        archives.exits = {"N" : None, "E" : None, "S" : None, "O" : None, "U" : secret_corridor, "D" : None}

        # Setup player and starting room

        self.player = Player(input("\nEntrez votre nom: "))
        self.player.current_room = hall

    # Play the game
    def play(self):
        self.setup()
        self.print_welcome()
        # Loop until the game is finished
        while not self.finished:
            # Get the command from the player
            self.process_command(input("> "))
        return None

    # Process the command entered by the player
    def process_command(self, command_string) -> None:

         # --- NOUVEAU : ignorer la commande vide ---
        if command_string.strip() == "":
            return  # ne rien afficher, ne rien faire

        # Split the command string into a list of words
        list_of_words = command_string.split(" ")

        command_word = list_of_words[0]

        # If the command is not recognized, print an error message
        if command_word not in self.commands.keys():
            print(f"\nCommande '{command_word}' non reconnue. Entrez 'help' pour voir la liste des commandes disponibles.\n")
        # If the command is recognized, execute it
        else:
            command = self.commands[command_word]
            command.action(self, list_of_words, command.number_of_parameters)

    # Print the welcome message
    def print_welcome(self):
        print(f"\nBienvenue {self.player.name} dans ce jeu d'aventure !")
        print("Entrez 'help' si vous avez besoin d'aide.")
        #
        print(self.player.current_room.get_long_description())
    

def main():
    # Create a game object and play the game
    Game().play()
    

if __name__ == "__main__":
    main()

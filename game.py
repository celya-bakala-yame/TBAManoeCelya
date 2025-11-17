# game.py
from room import Room
from player import Player
from command import Command
from actions import Actions

class Game:

    def __init__(self):
        self.finished = False
        self.rooms = []
        self.commands = {}
        self.player = None
    
    def setup(self):

        # Setup commands (5 commandes : go, look, take, drop, talk)
        self.commands["go"] = Command("go", " <direction> : se déplacer", Actions.go, 1)
        self.commands["look"] = Command("look", " : examiner la salle ou un objet", Actions.look, 0)
        self.commands["take"] = Command("take", " <objet> : prendre un objet", Actions.take, 1)
        self.commands["drop"] = Command("drop", " <objet> : poser un objet", Actions.drop, 1)
        self.commands["talk"] = Command("talk", " <personnage> : parler à un PNJ", Actions.talk, 1)
        
        # Setup rooms
        hall = Room("Hall", "dans le hall d'entrée de la bibliothèque")
        reading_room = Room("Salle de lecture", "une grande salle avec des étagères remplies de livres")
        study1 = Room("Salle de travail 1", "une petite salle silencieuse")
        study2 = Room("Salle de travail 2", "une salle avec des tables pour étudier")
        study3 = Room("Salle de travail 3", "une salle lumineuse")
        study4 = Room("Salle de travail 4", "une salle calme avec quelques étudiants")
        librarian_office = Room("Bureau du bibliothécaire", "le bureau du bibliothécaire")
        secret_corridor = Room("Couloir secret", "un passage caché derrière le bureau")
        archives = Room("Salle des archives", "une pièce où se cache le livre rare")
        
        # Relier les pièces
        hall.exits = {"N": reading_room}
        reading_room.exits = {"S": hall, "E": study1, "O": study2, "N": study3, "NE": study4, "NW": librarian_office}
        librarian_office.exits = {"S": reading_room, "N": secret_corridor}
        secret_corridor.exits = {"S": librarian_office, "N": archives}
        # Autres salles peuvent être reliées si nécessaire...
        
        # Ajouter les salles dans la liste
        self.rooms.extend([hall, reading_room, study1, study2, study3, study4, librarian_office, secret_corridor, archives])

        # Setup player
        self.player = Player(input("\nEntrez votre nom: "))
        self.player.current_room = hall

    def play(self):
        self.setup()
        self.print_welcome()
        while not self.finished:
            self.process_command(input("> "))

    def process_command(self, command_string):
        list_of_words = command_string.split()
        if len(list_of_words) == 0:
            return
        command_word = list_of_words[0]
        if command_word not in self.commands:
            print(f"\nCommande '{command_word}' non reconnue.\n")
        else:
            command = self.commands[command_word]
            command.action(self, list_of_words, command.number_of_parameters)

    def print_welcome(self):
        print(f"\nBienvenue {self.player.name} dans ce jeu d'aventure !")
        print("Utilisez 'go', 'look', 'take', 'drop', 'talk' pour interagir avec l'environnement.\n")
        print(self.player.current_room.get_long_description())

def main():
    Game().play()

if __name__ == "__main__":
    main()

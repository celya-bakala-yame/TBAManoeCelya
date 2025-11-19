from room import Room
from player import Player
from command import Command
from actions import Actions
from character import Character
from item import Item

class Game:

    def __init__(self):
        self.finished = False
        self.rooms = []
        self.commands = {}
        self.player = None

    def setup(self):
        # --- COMMANDES ---
        self.commands["go"] = Command("go", " <direction> : se déplacer", Actions.go, 1)
        self.commands["look"] = Command("look", " : examiner la salle ou un objet", Actions.look, 0)
        self.commands["take"] = Command("take", " <objet> : prendre un objet", Actions.take, 1)
        self.commands["drop"] = Command("drop", " <objet> : poser un objet", Actions.drop, 1)
        self.commands["talk"] = Command("talk", " <personnage> : parler à un PNJ", Actions.talk, 1)

        # --- SALLES ---
        hall = Room("Hall", "le hall d'entrée spacieux")
        library = Room("Salle de lecture", "une grande bibliothèque calme mais un peu sombre")
        study1 = Room("Salle de travail 1", "une petite salle silencieuse")
        study2 = Room("Salle de travail 2", "une salle avec un étudiant perdu")
        study3 = Room("Salle de travail 3", "une salle avec une clé cassée sur une table")
        study4 = Room("Salle de travail 4", "une salle calme avec un fantôme mystérieux")
        librarian_office = Room("Bureau du bibliothécaire", "bureau du bibliothécaire, avec un tiroir verrouillé")
        secret_corridor = Room("Passage secret", "un couloir caché derrière le bureau")
        dark_corridor = Room("Couloir sombre", "une zone trop sombre pour avancer sans lampe")
        archives = Room("Salle des archives", "une pièce silencieuse avec des livres anciens")

        # --- EXITS ---
        hall.exits = {"N": library}
        library.exits = {"S": hall, "E": study1, "O": study2, "N": study3, "NE": study4, "NW": librarian_office}
        study1.exits = {"W": library}
        study2.exits = {"E": library}
        study3.exits = {"S": library}
        study4.exits = {"SW": library}
        librarian_office.exits = {"SE": library, "N": secret_corridor}
        secret_corridor.exits = {"S": librarian_office, "N": dark_corridor}
        dark_corridor.exits = {"S": secret_corridor, "N": archives}
        archives.exits = {"S": dark_corridor}

        # --- OBJETS ---
        hall.inventory.append(Item("Plan", "Plan du rez-de-chaussée"))
        library.inventory.append(Item("Lampe de poche", "Une lampe utile pour explorer les zones sombres"))
        library.inventory.append(Item("Livre ouvert", "Contient un indice crypté"))
        study1.inventory.append(Item("Note chiffonnée", "Indice sur la clé du bureau"))
        study2.inventory.append(Item("Stylo oublié", "Juste un objet décoratif"))
        study3.inventory.append(Item("Clé cassée", "Objet pour tromper le joueur"))
        librarian_office.inventory.append(Item("Clé du passage secret", "Permet d'ouvrir le passage secret"))
        librarian_office.inventory.append(Item("Dossier poussiéreux", "Juste décoratif"))
        secret_corridor.inventory.append(Item("Toile d’araignée", "Décor"))
        secret_corridor.inventory.append(Item("Niche murale", "Message crypté à l'intérieur"))
        dark_corridor.inventory.append(Item("Obscurité", "Il fait trop sombre pour voir"))
        archives.inventory.append(Item("Livre rare", "L'objet final du jeu"))
        archives.inventory.append(Item("Livre faux", "Pour piéger le joueur"))
        archives.inventory.append(Item("Boîte d’archives", "Décor"))

        # --- PNJ ---
        hall.characters.append(Character("Étudiant stressé", "il semble perdu et inquiet", hall, ["Euh… bonjour… je… je cherche la sortie ?"]))
        library.characters.append(Character("Étudiante qui lit", "une étudiante concentrée", library, ["Le savoir se cache dans les livres poussiéreux."]))
        study2.characters.append(Character("Étudiant perdu", "il semble avoir oublié quelque chose", study2, ["Peut-être que la clé est ailleurs… ou pas."]))
        study4.characters.append(Character("Fantôme", "apparition mystérieuse", study4, ["Ce que tu cherches est caché derrière les mots… Suis la poussière du temps."]))
        librarian_office.characters.append(Character("Bibliothécaire", "un vieil homme avec des lunettes rondes", librarian_office, [
            "Bonjour ! As-tu besoin d'aide pour trouver un livre ?",
            "Le secret se cache peut-être dans les archives..."
        ]))

        # --- AJOUTER LES SALLES À LA LISTE ---
        self.rooms.extend([hall, library, study1, study2, study3, study4, librarian_office, secret_corridor, dark_corridor, archives])

        # --- PLAYER ---
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

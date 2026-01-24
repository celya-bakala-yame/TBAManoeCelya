"""Game class"""

# Import modules

from room import Room, Door, Drawer
from player import Player
from command import Command
from actions import Actions
from item import Item
from character import Character
from quest import Quest


class Game:
    """The Game class manages the overall game state and flow."""
    
    # Constructor
    def __init__(self):
        self.finished = False
        self.rooms = []
        self.commands = {}
        self.player = None
        self.items = []
    
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
        back = Command("back", " : revenir à la pièce précédente", Actions.back, 0)
        self.commands["back"] = back
        look = Command("look"," : observer la pièce et les objets présents", Actions.look, 0)
        self.commands["look"] = look
        take = Command("take", " <nom_item> : prendre un item et l'ajouter à votre inventaire", Actions.take, 1)
        self.commands["take"] = take
        drop = Command("drop", " <nom_item> : déposer un item de votre inventaire dans la salle", Actions.drop, 1)
        self.commands["drop"] = drop
        check = Command("check", " : afficher le contenu de votre inventaire", Actions.check, 0)
        self.commands["check"] = check
        talk = Command("talk", " <nom_pnj> : parler à un personnage non joueur", Actions.talk, -1)
        self.commands["talk"] = talk
        quests = Command("quests", " : afficher la liste des quêtes", Actions.quests, 0)
        self.commands["quests"] = quests
        quest = Command("quest", " <titre> : afficher les détails d'une quête", Actions.quest, 1)
        self.commands["quest"] = quest
        activate = Command("activate", " <titre> : activer une quête", Actions.activate, 1)
        self.commands["activate"] = activate
        rewards = Command("rewards", " : afficher vos récompenses", Actions.rewards, 0)
        self.commands["rewards"] = rewards
        



        
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
        

        secret_corridor.door = Door(locked=True)
        librarian_office.drawer = Drawer(locked=True) # Tiroir du bureau du bibliothécaire
        

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
        self._setup_quests()
        
        # Setup items

        plan = Item("plan", "Plan du rez-de-chaussée (carte simple)", 0.1)
        self.items.append(plan)
        lampe = Item("lampe", "Lampe de poche", 0.3)
        self.items.append(lampe)
        livre_ouvert = Item("livre_ouvert", "Livre ouvert", 1)
        self.items.append(livre_ouvert)
        note_chiffonnee = Item("note_chiffonnee", "Note chiffonnée", 0.05)
        self.items.append(note_chiffonnee)
        stylo_oublie = Item("stylo_oublie", "Stylo oublié", 0.05)
        self.items.append(stylo_oublie)
        cle_tiroir = Item("cle_tiroir", "Clé du tiroir vérrouillé", 0.05)
        self.items.append(cle_tiroir)
        cle_passage_secret = Item("cle_passage_secret", "Clé du passage secret", 0.05)
        self.items.append(cle_passage_secret)
        dossier_poussiereux = Item("dossier_poussiereux", "Dossier poussiéreux", 0.5)
        self.items.append(dossier_poussiereux)
        tiroir_verrouille = Item("tiroir_verrouille", "Un tiroir verrouillé", 2)
        self.items.append(tiroir_verrouille)
        affiche_cryptee = Item("affiche_cryptee", "Affiche avec message crypté", 0.2)
        self.items.append(affiche_cryptee)
        livre_rare = Item("livre_rare", "Livre rare", 1.2)
        self.items.append(livre_rare)
        livre_faux = Item("livre_faux", "Livre faux", 1)
        self.items.append(livre_faux)
        boite_archives = Item("boite_archives", "Boîte d’archives fermée", 1)
        self.items.append(boite_archives)

        librarian_office.drawer_key = cle_passage_secret
        # Setup inventory of rooms

        hall.inventory.append(plan)
        library.inventory.append(lampe)
        library.inventory.append(livre_ouvert)
        study1.inventory.append(note_chiffonnee)
        study2.inventory.append(stylo_oublie)
        study3.inventory.append(cle_tiroir)
        librarian_office.inventory.append(dossier_poussiereux)
        librarian_office.inventory.append(tiroir_verrouille)
        secret_corridor.inventory.append(affiche_cryptee)
        archives.inventory.append(livre_rare)
        archives.inventory.append(livre_faux)
        archives.inventory.append(boite_archives)

        fantome = Character(
            "fantome",
            "un esprit pâle qui flotte silencieusement",
            study4,
            ["Certains secrets ne s’ouvrent qu’avec la bonne clé."]
        )

        etudiant = Character(
            "etudiant_perdu",
            "un étudiant visiblement stressé",
            study2,
            ["J’ai vu une clé quelque part plus loin..."]
        )

        bibliothecaire = Character(
            "bibliothecaire",
            "un homme sévère qui garde le bureau",
            librarian_office,
            ["Ce n’est pas parce qu’un tiroir est fermé qu’il est vide."]
        )
        
        bibliothecaire.can_move = False
        study4.characters.append(fantome)
        study2.characters.append(etudiant)
        librarian_office.characters.append(bibliothecaire)

    def _setup_quests(self):
        """Initialize all quests."""
        exploration_quest = Quest(
            title="Le Tour de la Bibliothèque",
            description="Explorez toutes les salles principales de la bibliothèque.",
            objectives=[
                "Visiter Hall",
                "Visiter Salle de lecture",
                "Visiter Salle de travail 1",
                "Visiter Salle de travail 2",
                "Visiter Salle de travail 3",
                "Visiter Salle de travail 4",
            ],
            reward="Plan annoté"
        )

        interaction_quest = Quest(
            title="Le Bibliothécaire Suspicionneux",
            description="Trouvez le secret que garde le bibliothécaire.",
            objectives=[
                "prendre cle_tiroir",
                "parler avec bibliothecaire",
            ],
            reward="Indication secrète"
        )

        item_quest = Quest(
            title="Le Livre Interdit",
            description="Trouvez le vrai livre rare caché dans les archives.",
            objectives=[
                "Visiter Bureau du bibliothécaire",
                "prendre cle_passage_secret",
                "Visiter Passage secret",
                "Visiter Salle des archives",
                "prendre livre_rare",
            ],
            reward="Livre ancien"
        )

        self.player.quest_manager.add_quest(exploration_quest)
        self.player.quest_manager.add_quest(interaction_quest)
        self.player.quest_manager.add_quest(item_quest)

    def win(self):
        """
        Check if the player has won the game.
        
        Returns:
            bool: True if all quests are completed, False otherwise.
        """
        quests = self.player.quest_manager.get_all_quests()

        # S'il n'y a aucune quête, on ne peut pas gagner
        if not quests:
            return False

        # Vérifie que toutes les quêtes sont terminées
        return all(quest.is_completed for quest in quests)

    def loose(self) -> bool:
        """
        Check if the player has lost the game.

        Example rule:
        - If the player enters 'Salle des archives' without the 'lampe', they lose.
        """
        # Défaite seulement si on est dans une pièce précise
        if self.player.current_room.name != "Salle des archives":
            return False

        # Vérifier la possession d'un objet précis
        has_lampe = any(getattr(it, "name", "") == "lampe" for it in self.player.inventory)
        return not has_lampe

    # Play the game
    def play(self):
        """Main game loop."""
        
        self.setup()
        self.print_welcome()
        # Loop until the game is finished
        while not self.finished:
            self.process_command(input("> "))

            if self.loose():
                print("\n💀 Vous avancez dans les archives dans le noir... quelque chose vous tombe dessus.")
                print("😵 Vous avez perdu la partie.\n")
                self.finished = True
                break

            # Vérifier condition de victoire
            if self.win():
                print("\n🏆 Félicitations ! Vous avez terminé toutes les quêtes !")
                print("🎉 Vous avez gagné la partie !\n")
                self.finished = True
        return None

    # Process the command entered by the player
    def process_command(self, command_string) -> None:
        """Process the command entered by the player."""

         # --- NOUVEAU : ignorer la commande vide ---
        if command_string.strip() == "":
            return  # ne rien afficher, ne rien faire

        # Split the command string into a list of words
        

        # If the command is not recognized, print an error message
    

        list_of_words = command_string.split(" ")

        command_word = list_of_words[0]
        if command_word not in self.commands.keys():
            print(f"\nCommande '{command_word}' non reconnue. Entrez 'help' pour voir la liste des commandes disponibles.\n")
        # If the command is recognized, execute it
        else:
            command = self.commands[command_word]
            command.action(self, list_of_words, command.number_of_parameters)
        all_characters = []
        for room in self.rooms:
            all_characters.extend(room.characters)

        for character in all_characters:
            character.move()

    # Print the welcome message
    def print_welcome(self):
        """Print the welcome message."""
        
        print(f"\nBienvenue {self.player.name} dans ce jeu d'aventure !")
        print("Entrez 'help' si vous avez besoin d'aide.")
        #
        print(self.player.current_room.get_long_description())


def main():
    """Create a game object and play the game"""
    Game().play()
    

if __name__ == "__main__":
    main()

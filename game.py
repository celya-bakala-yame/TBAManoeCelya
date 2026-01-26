"""Game class"""

# Import modules

from room import Room, Door, Drawer
from player import Player
from command import Command
from actions import Actions
from item import Item
from character import Character
from quest import Quest
import sys
from pathlib import Path
import tkinter as tk
from tkinter import ttk, simpledialog



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
    def setup(self, player_name=None):



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
        quest = Command("quest", " <titre> : afficher les détails d'une quête", Actions.quest, -1)
        self.commands["quest"] = quest
        activate = Command("activate", " <titre> : activer une quête", Actions.activate, -1)
        self.commands["activate"] = activate
        rewards = Command("rewards", " : afficher vos récompenses", Actions.rewards, 0)
        self.commands["rewards"] = rewards
        



        
        # Setup rooms

        hall = Room("Hall", "le hall d'entrée spacieux.",  image = "hall.png")
        self.rooms.append(hall)
        library = Room("Salle de lecture", "une grande bibliothèque calme mais un peu sombre.",  image = "library.png")
        self.rooms.append(library)
        study1 = Room("Salle de travail 1", "une petite salle silencieuse.",  image = "study1.png")
        self.rooms.append(study1)
        study2 = Room("Salle de travail 2", "une salle avec un étudiant perdu.",  image = "study2.png")
        self.rooms.append(study2)
        study3 = Room("Salle de travail 3", "une salle avec une clé cassée sur une table.", image = "study3.png")
        self.rooms.append(study3)
        study4 = Room("Salle de travail 4", "une salle calme avec un fantôme mystérieux.", image = "study4.png")
        self.rooms.append(study4)
        librarian_office = Room("Bureau du bibliothécaire", "le bureau du bibliothécaire, avec un tiroir verrouillé.", image = "librarian_office.png")
        self.rooms.append(librarian_office)
        secret_corridor = Room("Passage secret", "un couloir caché derrière le bureau.", image= "secret_corridor.png")
        self.rooms.append(secret_corridor)
        archives = Room("Salle des archives", "une pièce silencieuse avec des livres anciens.", image ="archives.png")
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

        if player_name is None:
            player_name = input("\nEntrez votre nom: ")
        self.player = Player(player_name)
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


        # Add quests to player's quest manager
        self.player.quest_manager.add_quest(exploration_quest)
        self.player.quest_manager.add_quest(interaction_quest)
        self.player.quest_manager.add_quest(item_quest)

    def win(self) -> bool:
        """
        Vérifie si le joueur a gagné la partie.

        Returns:
            bool: True si toutes les quêtes sont terminées, False sinon.
        """
        quests = self.player.quest_manager.get_all_quests()

        # S'il n'y a aucune quête, on ne peut pas gagner
        if not quests:
            return False

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

            if self.win():
                print("\n🏆 Félicitations ! Vous avez terminé toutes les quêtes !")
                print("🎉 Vous avez gagné la partie !\n")
                self.finished = True
                break

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
    
class _StdoutRedirector:
    """Redirect sys.stdout writes into a Tkinter Text widget."""
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, msg):
        """Write message to the Text widget."""
        if msg:
            self.text_widget.configure(state="normal")
            self.text_widget.insert("end", msg)
            self.text_widget.see("end")
            self.text_widget.configure(state="disabled")

    def flush(self):
        """Flush method required by sys.stdout interface (no-op for Text widget)."""


class GameGUI(tk.Tk):
    """Tkinter GUI for the text-based adventure game.

    Layout layers:
    L3 (top): Split into left image area (600x400) and right buttons.
    L2 (middle): Scrolling terminal output.
    L1 (bottom): Command entry field.
    """

    IMAGE_WIDTH = 600
    IMAGE_HEIGHT = 400

    def __init__(self):
        super().__init__()
        self.title("TBA")
        self.geometry("900x700")  # Provide enough space
        self.minsize(900, 650)

        # Underlying game logic instance
        self.game = Game()

        # Ask player name via dialog (fallback to 'Joueur')
        name = simpledialog.askstring("Nom", "Entrez votre nom:", parent=self)
        if not name:
            name = "Joueur"
        self.game.setup(player_name=name)  # Pass name to avoid double prompt

        # Build UI layers
        self._build_layout()

        # Redirect stdout so game prints appear in terminal output area
        self.original_stdout = sys.stdout
        sys.stdout = _StdoutRedirector(self.text_output)

        # Print welcome text in GUI
        self.game.print_welcome()

        # Load initial room image
        self._update_room_image()

        # Handle window close
        self.protocol("WM_DELETE_WINDOW", self._on_close)


    # -------- Layout construction --------
    def _build_layout(self):
        # Configure root grid: 3 rows (L3, L2, L1)
        self.grid_rowconfigure(0, weight=0)  # Image/buttons fixed height
        self.grid_rowconfigure(1, weight=1)  # Terminal output expands
        self.grid_rowconfigure(2, weight=0)  # Entry fixed
        self.grid_columnconfigure(0, weight=1)

        # L3 Top frame
        top_frame = ttk.Frame(self)
        top_frame.grid(row=0, column=0, sticky="nsew", padx=6, pady=(6,3))
        top_frame.grid_columnconfigure(0, weight=0)
        top_frame.grid_columnconfigure(1, weight=1)

        # L3L Image area (left)
        image_frame = ttk.Frame(top_frame, width=self.IMAGE_WIDTH, height=self.IMAGE_HEIGHT)
        image_frame.grid(row=0, column=0, sticky="nw", padx=(0,6))
        image_frame.grid_propagate(False)  # Keep requested size
        self.canvas = tk.Canvas(image_frame,
                                width=self.IMAGE_WIDTH,
                                height=self.IMAGE_HEIGHT,
                                bg="#222")
        self.canvas.pack(fill="both", expand=True)

        # Initialize image reference (will be loaded by _update_room_image)
        self._image_ref = None  # Keep reference to prevent garbage collection
        # Initial image will be loaded after welcome message

        # L3R Buttons area (right)
        buttons_frame = ttk.Frame(top_frame)
        buttons_frame.grid(row=0, column=1, sticky="ne")
        for i in range(10):
            buttons_frame.grid_rowconfigure(i, weight=0)
        buttons_frame.grid_columnconfigure(0, weight=1)

        # Load button images (keep references to prevent garbage collection)
        assets_dir = Path(__file__).parent / 'assets'
        # Load pre-resized 50x50 PNG images for better quality
        self._btn_help = tk.PhotoImage(file=str(assets_dir / 'help-50.png'))
        self._btn_up = tk.PhotoImage(file=str(assets_dir / 'up-arrow-50.png'))
        self._btn_down = tk.PhotoImage(file=str(assets_dir / 'down-arrow-50.png'))
        self._btn_left = tk.PhotoImage(file=str(assets_dir / 'left-arrow-50.png'))
        self._btn_right = tk.PhotoImage(file=str(assets_dir / 'right-arrow-50.png'))
        self._btn_quit = tk.PhotoImage(file=str(assets_dir / 'quit-50.png'))

        # Command buttons
        tk.Button(buttons_frame,
                  image=self._btn_help,
                  command=lambda: self._send_command("help"),
                  bd=0).grid(row=0, column=0, sticky="ew", pady=2)
        # Movement buttons (N,E,S,O)
        move_frame = ttk.LabelFrame(buttons_frame, text="Déplacements")
        move_frame.grid(row=1, column=0, sticky="ew", pady=4)
        tk.Button(move_frame,
                  image=self._btn_up,
                  command=lambda: self._send_command("go N"),
                  bd=0).grid(row=0, column=0, columnspan=2)
        tk.Button(move_frame,
                  image=self._btn_left,
                  command=lambda: self._send_command("go O"),
                  bd=0).grid(row=1, column=0)
        tk.Button(move_frame,
                  image=self._btn_right,
                  command=lambda: self._send_command("go E"),
                  bd=0).grid(row=1, column=1)
        tk.Button(move_frame,
                  image=self._btn_down,
                  command=lambda: self._send_command("go S"),
                  bd=0).grid(row=2, column=0, columnspan=2)

        # Quit button
        tk.Button(buttons_frame,
                  image=self._btn_quit,
                  command=lambda: self._send_command("quit"),
                  bd=0).grid(row=2, column=0, sticky="ew", pady=(8,2))

        # L2 Terminal output area (Text + Scrollbar)
        output_frame = ttk.Frame(self)
        output_frame.grid(row=1, column=0, sticky="nsew", padx=6, pady=3)
        output_frame.grid_rowconfigure(0, weight=1)
        output_frame.grid_columnconfigure(0, weight=1)

        scrollbar = ttk.Scrollbar(output_frame, orient="vertical")
        self.text_output = tk.Text(output_frame,
                                   wrap="word",
                                   yscrollcommand=scrollbar.set,
                                   state="disabled",
                                   bg="#111", fg="#eee")
        scrollbar.config(command=self.text_output.yview)
        self.text_output.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # L1 Entry area
        entry_frame = ttk.Frame(self)
        entry_frame.grid(row=2, column=0, sticky="ew", padx=6, pady=(3,6))
        entry_frame.grid_columnconfigure(0, weight=1)

        self.entry_var = tk.StringVar()
        self.entry = ttk.Entry(entry_frame, textvariable=self.entry_var)
        self.entry.grid(row=0, column=0, sticky="ew")
        self.entry.bind("<Return>", self._on_enter)
        self.entry.focus_set()


    # -------- Image update --------
    def _update_room_image(self):
        """Update the canvas image based on the current room."""
        if not self.game.player or not self.game.player.current_room:
            return

        room = self.game.player.current_room
        assets_dir = Path(__file__).parent / 'assets'

        # Use room-specific image if available, otherwise fallback
        if room.image:
            image_path = assets_dir / room.image
        else:
            image_path = assets_dir / 'scene.png'

        try:
            # Load new image
            self._image_ref = tk.PhotoImage(file=str(image_path))
            # Clear canvas and redraw image
            self.canvas.delete("all")
            self.canvas.create_image(
                self.IMAGE_WIDTH/2,
                self.IMAGE_HEIGHT/2,
                image=self._image_ref
            )
        except (FileNotFoundError, tk.TclError):
            # Fallback to text if image not found or cannot be loaded
            self.canvas.delete("all")
            self.canvas.create_text(
                self.IMAGE_WIDTH/2,
                self.IMAGE_HEIGHT/2,
                text=f"Image: {room.name}",
                fill="white",
                font=("Helvetica", 18)
            )


    # -------- Event handlers --------
    def _on_enter(self, _event=None):
        """Handle Enter key press in the entry field."""
        value = self.entry_var.get().strip()
        if value:
            self._send_command(value)
        self.entry_var.set("")


    def _send_command(self, command):
        if self.game.finished:
            return
        # Echo the command in output area
        print(f"> {command}\n")
        self.game.process_command(command)
        # Update room image after command (in case player moved)
        self._update_room_image()
        if self.game.finished:
            # Disable further input and schedule close (brief delay to show farewell)
            self.entry.configure(state="disabled")
            self.after(600, self._on_close)


    def _on_close(self):
        # Restore stdout and destroy window
        sys.stdout = self.original_stdout
        self.destroy()


def main():
    """Entry point.

    If '--cli' is passed as an argument, start the classic console version.
    Otherwise launch the Tkinter GUI.
    Fallback to CLI if GUI cannot be initialized (e.g., headless environment).
    """
    args = sys.argv[1:]
    if '--cli' in args:
        Game().play()
        return
    try:
        app = GameGUI()
        app.mainloop()
    except tk.TclError as e:
        # Fallback to CLI if GUI fails (e.g., no DISPLAY, Tkinter not available)
        print(f"GUI indisponible ({e}). Passage en mode console.")
        Game().play()


if __name__ == "__main__":
    main()



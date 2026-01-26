"""The actions module"""

# The actions module contains the functions that are called when a command is executed.
# Each function takes 3 parameters:
# - game: the game object
# - list_of_words: the list of words in the command
# - number_of_parameters: the number of parameters expected by the command
# The functions return True if the command was executed successfully, False otherwise.
# The functions print an error message if the number of parameters is incorrect.
# The error message is different depending on the number of parameters expected by the command.


# The error message is stored in the MSG0 and MSG1 variables and formatted
# with the command_word variable, and the first word in the command. 
# The MSG0 variable is used when the command does not take any parameter.
MSG0 = "\nLa commande '{command_word}' ne prend pas de paramètre.\n"
# The MSG1 variable is used when the command takes 1 parameter.
MSG1 = "\nLa commande '{command_word}' prend 1 seul paramètre.\n"

class Actions:

    """
    The Actions class contains static methods that define the actions
    that can be performed in the game.
    """

    VALID_DIRECTIONS = {
        "N": "N", "NORD": "N",
        "S": "S", "SUD": "S",
        "E": "E", "EST": "E",
        "O": "O", "OUEST": "O",
        "U": "U", "UP": "U",
        "D": "D", "DOWN": "D"
    }

    def go(game, list_of_words, number_of_parameters):
        """
        Move the player in the direction specified by the parameter.
        The parameter must be a cardinal direction (N, E, S, O).

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:
        
        >>> from game import Game
        >>> game = Game()
        >>> game.setup("TestPlayer")
        >>> Actions.go(game, ["go", "N"], 1)
        <BLANKLINE>
        Vous êtes dans une immense tour en pierre qui s'élève au dessus des nuages.
        <BLANKLINE>
        Sorties: N, S, O
        <BLANKLINE>
        True
        >>> Actions.go(game, ["go", "N", "E"], 1)
        <BLANKLINE>
        La commande 'go' prend 1 seul paramètre.
        <BLANKLINE>
        False
        >>> Actions.go(game, ["go"], 1)
        <BLANKLINE>
        La commande 'go' prend 1 seul paramètre.
        <BLANKLINE>
        False

        """
        
        player = game.player
        l = len(list_of_words)
        # If the number of parameters is incorrect, print an error message and return False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        # Get the direction from the list of words.
        direction = list_of_words[1].upper()
        if direction not in Actions.VALID_DIRECTIONS:
           print("Cette direction n'est pas valide.")
           return False
        # Move the player in the direction specified by the parameter.
        final_direction = Actions.VALID_DIRECTIONS[direction]
        player.move(final_direction)
        return True


    @staticmethod
    def quit(game, list_of_words, number_of_parameters):
        """
        Quit the game.

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup("TestPlayer")
        >>> Actions.quit(game, ["quit"], 0)
        <BLANKLINE>
        Merci TestPlayer d'avoir joué. Au revoir.
        <BLANKLINE>
        True
        >>> Actions.quit(game, ["quit", "N"], 0)
        <BLANKLINE>
        La commande 'quit' ne prend pas de paramètre.
        <BLANKLINE>
        False
        >>> Actions.quit(game, ["quit", "N", "E"], 0)
        <BLANKLINE>
        La commande 'quit' ne prend pas de paramètre.
        <BLANKLINE>
        False

        """
        l = len(list_of_words)
        # If the number of parameters is incorrect, print an error message and return False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
        # Set the finished attribute of the game object to True.
        player = game.player
        msg = f"\nMerci {player.name} d'avoir joué. Au revoir.\n"
        print(msg)
        game.finished = True
        return True
        
    @staticmethod
    def help(game, list_of_words, number_of_parameters):
        """
        Print the list of available commands.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup("TestPlayer")
        >>> Actions.help(game, ["help"], 0) # doctest: +NORMALIZE_WHITESPACE
        <BLANKLINE>
        Voici les commandes disponibles:
            - help : afficher cette aide
            - quit : quitter le jeu
            - go <direction> : se déplacer dans une direction cardinale (N, E, S, O)
            - quests : afficher la liste des quêtes
            - quest <titre> : afficher les détails d'une quête
            - activate <titre> : activer une quête
            - rewards : afficher vos récompenses
        <BLANKLINE>
        True
        >>> Actions.help(game, ["help", "N"], 0)
        <BLANKLINE>
        La commande 'help' ne prend pas de paramètre.
        <BLANKLINE>
        False
        >>> Actions.help(game, ["help", "N", "E"], 0)
        <BLANKLINE>
        La commande 'help' ne prend pas de paramètre.
        <BLANKLINE>
        False

        """

        # If the number of parameters is incorrect, print an error message and return False.
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
        # Print the list of available commands.
        print("\nVoici les commandes disponibles:")
        for command in game.commands.values():
            print("\t- " + str(command))
        print()
        return True
        
    @staticmethod
    def history(game, words, number_of_parameters):
        """
        Affiche l’historique des salles visitées par le joueur.
        
        """
        print(game.player.get_history())
        return False

    def back(game, list_of_words, number_of_parameters):
        """
        Permet de revenir à la pièce précédente, si possible.
        
        Args:
            game (Game): L'objet de jeu.
            list_of_words (list): Liste des mots dans la commande.
            number_of_parameters (int): Le nombre de paramètres attendus par la commande.

        Returns:
            bool: True si la commande a été exécutée avec succès, False sinon.
        """

        l = len(list_of_words)
        # Vérifie que la commande ne prend pas de paramètres
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        player = game.player
        # Si l'historique est vide, le joueur ne peut pas revenir en arrière
        if not player.history:
            print("\nVous n'avez encore visité aucune autre pièce.\n")
            return False
    
        # Revenir à la dernière pièce visitée
        previous_room = player.history.pop()  # Retirer la dernière pièce de l'historique
        player.current_room = previous_room
        print(f"\nVous êtes maintenant dans : {player.current_room.get_long_description()}")
        return True

    def look(game, params, n_params):
        """
        Affiche la description de la salle, les PNJ et les items présents.
        """
        room = game.player.current_room

        # Affiche la description complète de la salle
        first_line = room.get_long_description().strip().split("\n")[0]
        print("\n" + first_line + "\n")

        # S'il y a des personnages ou des items
        if room.characters or room.inventory:
            print("La pièce contient :")

            # Afficher les PNJ
            for character in room.characters:
                print(f"    - {character}")

            # Afficher les items
            for item in room.inventory:
                print(f"    - {item}")

            print()
        else:
            print("Il n'y a rien ici.\n")

    def take(game, params, n_params):
        if len(params) < 2:
            print("Précisez l'item à prendre. Exemple : take lampe")
            return False

        item_name = params[1].strip().lower()
        game.player.take(item_name)

        # Valider seulement si l'objet est bien dans l'inventaire (comparaison en minuscule)
        if any(getattr(it, "name", "").lower() == item_name for it in game.player.inventory):
            game.player.quest_manager.check_action_objectives("prendre", item_name)
            return True

        return False

    
    def drop(game, params, n_params):
        """
        Commande drop : permet au joueur de déposer un item dans la salle.
        """
        if len(params) < 2:
            print("Précisez l'item à déposer. Exemple : drop lampe")
            return

        item_name = params[1]
        game.player.drop(item_name)

    def check(game, list_of_words, number_of_parameters):

        # Vérification du nombre de paramètres
        if len(list_of_words) != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        print("\n" + game.player.get_inventory() + "\n")
        return True

    def talk(game, words, n):
        if len(words) < 2:
            print("\nPrécisez le nom du personnage.\n")
            return False

        target = words[1].strip().lower()
        room = game.player.current_room

        for character in room.characters:
            if character.name.lower() == target:
                character.get_msg(game.player)
                game.player.quest_manager.check_action_objectives("parler", target)
                return True

        print(f"\nIl n’y a personne nommé '{target}' ici.\n")
        return False

    def quests(game, list_of_words, number_of_parameters):
        """
        Show all quests and their status.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup("TestPlayer")
        >>> Actions.quests(game, ["quests"], 0)
        <BLANKLINE>
        📋 Liste des quêtes:
          ❓ Grand Explorateur (Non activée)
          ❓ Grand Voyageur (Non activée)
          ❓ Découvreur de Secrets (Non activée)
        <BLANKLINE>
        True
        >>> Actions.quests(game, ["quests", "param"], 0)
        <BLANKLINE>
        La commande 'quests' ne prend pas de paramètre.
        <BLANKLINE>
        False

        """
        # If the number of parameters is incorrect, print an error message and return False.
        n = len(list_of_words)
        if n != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        # Show all quests
        game.player.quest_manager.show_quests()
        return True


    @staticmethod
    def quest(game, list_of_words, number_of_parameters):
        """
        Show details about a specific quest.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup("TestPlayer")
        >>> Actions.quest(game, ["quest", "Grand", "Voyageur"], 1)
        <BLANKLINE>
        📋 Quête: Grand Voyageur
        📖 Déplacez-vous 10 fois entre les lieux.
        <BLANKLINE>
        Objectifs:
          ⬜ Se déplacer 10 fois (Progression: 0/10)
        <BLANKLINE>
        🎁 Récompense: Bottes de voyageur
        <BLANKLINE>
        True
        >>> Actions.quest(game, ["quest"], 1)
        <BLANKLINE>
        La commande 'quest' prend 1 seul paramètre.
        <BLANKLINE>
        False

        """
        # If the number of parameters is incorrect, print an error message and return False.
        n = len(list_of_words)
        if n < number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        # Get the quest title from the list of words (join all words after command)
        quest_title = " ".join(list_of_words[1:])

        # Prepare current counter values to show progress
        current_counts = {
            "Se déplacer": game.player.move_count
        }

        # Show quest details
        game.player.quest_manager.show_quest_details(quest_title, current_counts)
        return True


    @staticmethod
    def activate(game, list_of_words, number_of_parameters):
        """
        Activate a specific quest.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup("TestPlayer")
        >>> Actions.activate(game, ["activate", "Grand", "Voyageur"], 1) # doctest: +ELLIPSIS
        <BLANKLINE>
        🗡️  Nouvelle quête activée: Grand Voyageur
        📝 Déplacez-vous 10 fois entre les lieux.
        <BLANKLINE>
        True
        >>> Actions.activate(game, ["activate"], 1)
        <BLANKLINE>
        La commande 'activate' prend 1 seul paramètre.
        <BLANKLINE>
        False

        """
        # If the number of parameters is incorrect, print an error message and return False.
        n = len(list_of_words)
        if n < number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        # Get the quest title from the list of words (join all words after command)
        quest_title = " ".join(list_of_words[1:])

        # Try to activate the quest
        if game.player.quest_manager.activate_quest(quest_title):
            return True

        msg1 = f"\nImpossible d'activer la quête '{quest_title}'. "
        msg2 = "Vérifiez le nom ou si elle n'est pas déjà active.\n"
        print(msg1 + msg2)
        # print(f"\nImpossible d'activer la quête '{quest_title}'. \
        #             Vérifiez le nom ou si elle n'est pas déjà active.\n")
        return False


    @staticmethod
    def rewards(game, list_of_words, number_of_parameters):
        """
        Display all rewards earned by the player.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup("TestPlayer")
        >>> Actions.rewards(game, ["rewards"], 0)
        <BLANKLINE>
        🎁 Aucune récompense obtenue pour le moment.
        <BLANKLINE>
        True
        >>> Actions.rewards(game, ["rewards", "param"], 0)
        <BLANKLINE>
        La commande 'rewards' ne prend pas de paramètre.
        <BLANKLINE>
        False
        """
        # If the number of parameters is incorrect, print an error message and return False.
        n = len(list_of_words)
        if n != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        # Show all rewards
        game.player.show_rewards()
        return True

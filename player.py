"""Define the Player class."""

from quest import QuestManager

class Player():
    """ Représente un joueur dans le jeu.

    Un Player possède :
    - un nom
    - une salle actuelle dans laquelle il se trouve. """

    # Define the constructor.
    def __init__(self, name):
        """ Initialise un nouveau joueur.

        Args:
            name (str): Le nom du joueur.

        Examples:
        
        >>> player = Player("Alice")
        >>> player.name
        'Alice'
        >>> player.move_count
        0
        >>> player.rewards
        []
        """

        self.name = name
        self.current_room = None
        self.history = []   # historique initialisé vide
        self.inventory = []      # inventaire initialisé vide
        self.max_weight = 2.5   # poids max transportable (en kg)
        self.move_count = 0
        self.quest_manager = QuestManager(self)
        self.rewards = []  # List to store earned rewards

    
    # Define the move method.
    def move(self, direction):
        """
        Move the player in the specified direction.
        
        Args:
            direction (str): The direction to move (N, E, S, O).
            
        Returns:
            bool: True if the move was successful, False otherwise.
            
        Examples:
        
        >>> from room import Room
        >>> player = Player("Dave")
        >>> room1 = Room("Room1", "in room 1")
        >>> room2 = Room("Room2", "in room 2")
        >>> room3 = Room("Room3", "in room 3")
        >>> room1.exits = {"N": room2, "E": None, "S": None, "O": None}
        >>> room2.exits = {"S": room1, "E": room3, "S": None, "O": None}
        >>> player.current_room = room1
        >>> player.move_count
        0
        >>> player.move("N")
        <BLANKLINE>
        Vous êtes in room 2
        <BLANKLINE>
        Sorties: E
        <BLANKLINE>
        True
        >>> player.move_count
        1
        >>> player.current_room.name
        'Room2'
        >>> player.move("E")
        <BLANKLINE>
        Vous êtes in room 3
        <BLANKLINE>
        Sorties:
        <BLANKLINE>
        True
        >>> player.move_count
        2
        """
        room = self.current_room
        next_room = room.exits.get(direction)

        # Aucune sortie
        if next_room is None:
            print("\nAucune porte dans cette direction !\n")
            return False

        
        #VERROU : vérifier si la DESTINATION a une porte verrouillée
        if next_room.door and next_room.door.locked:
            has_key = any(item.name == "cle_passage_secret" for item in self.inventory)

            if not has_key:
                print("\nLa porte est verrouillée. Il vous faut la clé du passage secret.\n")
                return False

            # Déverrouiller la porte
            next_room.door.locked = False
            print("\nVous avez déverrouillé la porte avec la clé du passage secret.\n")

        # Historique AVANT déplacement
        self.history.append(room)

        # Déplacement
        self.current_room = next_room
        print(self.current_room.get_long_description())
        print(self.get_history() + "\n")

        # Check room visit objectives
        self.quest_manager.check_room_objectives(self.current_room.name)

        # Increment move counter and check movement objectives
        self.move_count += 1
        self.quest_manager.check_counter_objectives("Se déplacer", self.move_count)

        return True

    def get_history(self):
        """Retourne une chaîne de caractères représentant les pièces visitées."""

        if not self.history:
            return "Vous n'avez encore visité aucune autre pièce."

        lines = ["Vous avez déja visité les pièces suivantes :"]
        for room in self.history:
            # On récupère uniquement la première ligne de la description
            first_line = room.get_long_description().strip().split("\n")[0]
            lines.append("    - " + first_line)

        return "\n".join(lines)
    

    def get_inventory(self):
        """Retourne une chaîne de caractères représentant les objets du joueur."""

        if not self.inventory:
            return f"Votre inventaire est vide (0.00 / {self.max_weight:.2f} kg)."

        lines = [
            f"Vous disposez des items suivants ({self.get_inventory_weight():.2f} / {self.max_weight:.2f} kg) :"
        ]
        for item in self.inventory:
            lines.append("    - " + str(item))

        return "\n".join(lines)

    
    def take(self, item_name):
        """
        Prend un item depuis la salle actuelle et le met dans l'inventaire du joueur
        si le poids le permet.
        """
        room = self.current_room

        # Cherche l'item dans la salle
        item_to_take = None
        for item in room.inventory:
            if item.name.lower() == item_name.lower():
                item_to_take = item
                break

        if not item_to_take:
            print(f"\nL'item '{item_name}' n'est pas présent dans cette salle.\n")
            return
        
        if item_to_take.name == "tiroir_verrouille" and room.drawer :
            if room.drawer.locked:
                has_key = any(it.name == "cle_tiroir" for it in self.inventory)

                if not has_key:
                    print("\nLe tiroir est verrouillé. Il vous faut la clé du tiroir.\n")
                    return
                
                room.drawer.locked = False
                print("\nVous avez déverrouillé le tiroir avec la clé.\n")

                if hasattr(room, "drawer_key") and room.drawer_key:
                    room.inventory.append(room.drawer_key)
                    print("Quelque chose se trouve dans le tiroir...\n")
                    room.drawer_key = None

        # Vérification du poids
        current_weight = self.get_inventory_weight()
        if current_weight + item_to_take.weight > self.max_weight:
            print(
                f"\nImpossible de prendre '{item_to_take.name}' : "
                f"poids maximum dépassé ({current_weight:.2f} / {self.max_weight:.2f} kg).\n"
            )
            return

        # Prendre l'objet
        room.inventory.remove(item_to_take)
        self.inventory.append(item_to_take)
        print(f"\nVous avez pris l'objet '{item_to_take.name}'.\n")

    def drop(self, item_name):
        """
        Dépose un item depuis l'inventaire du joueur dans la salle actuelle.
        
        Args:
            item_name (str): le nom de l'item à déposer
        """
        # Cherche l'item dans l'inventaire du joueur
        item_to_drop = None
        for item in self.inventory:
            if item.name.lower() == item_name.lower():
                item_to_drop = item
                break

        if item_to_drop:
            # Retirer de l'inventaire du joueur
            self.inventory.remove(item_to_drop)
            # Ajouter à la salle
            self.current_room.inventory.append(item_to_drop)
            print("\n" + f"Vous avez déposé l'objet '{item_to_drop.name}'" + "\n")
        else:
            print("\n" + f"L'item '{item_name}' n'est pas dans votre inventaire." + "\n")

    def get_inventory_weight(self):
        """Retourne le poids total des objets transportés."""

        total = 0
        for item in self.inventory:
            total += item.weight
        return total

    def add_reward(self, reward):
        """
        Add a reward to the player's rewards list.
        
        Args:
            reward (str): The reward to add.
            
        Examples:
        
        >>> player = Player("Bob")
        >>> player.add_reward("Épée magique") # doctest: +NORMALIZE_WHITESPACE
        <BLANKLINE>
        🎁 Vous avez obtenu: Épée magique
        <BLANKLINE>
        >>> "Épée magique" in player.rewards
        True
        >>> player.add_reward("Épée magique") # Adding same reward again
        >>> len(player.rewards)
        1
        """
        if reward and reward not in self.rewards:
            self.rewards.append(reward)
            print(f"\n🎁 Vous avez obtenu: {reward}\n")


    def show_rewards(self):
        """
        Display all rewards earned by the player.
        
        Examples:
        
        >>> player = Player("Charlie")
        >>> player.show_rewards() # doctest: +NORMALIZE_WHITESPACE
        <BLANKLINE>
        🎁 Aucune récompense obtenue pour le moment.
        <BLANKLINE>
        >>> player.add_reward("Bouclier d'or") # doctest: +NORMALIZE_WHITESPACE
        <BLANKLINE>
        🎁 Vous avez obtenu: Bouclier d'or
        <BLANKLINE>
        >>> player.show_rewards() # doctest: +NORMALIZE_WHITESPACE
        <BLANKLINE>
        🎁 Vos récompenses:
        • Bouclier d'or
        <BLANKLINE>
        """
        if not self.rewards:
            print("\n🎁 Aucune récompense obtenue pour le moment.\n")
        else:
            print("\n🎁 Vos récompenses:")
            for reward in self.rewards:
                print(f"  • {reward}")
            print()

    


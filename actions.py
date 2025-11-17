# actions.py
MSG0 = "\nLa commande '{command_word}' ne prend pas de paramètre.\n"
MSG1 = "\nLa commande '{command_word}' prend 1 seul paramètre.\n"

class Actions:

    def go(game, list_of_words, number_of_parameters):
        player = game.player
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False
        direction = list_of_words[1]
        return player.move(direction)

    def look(game, list_of_words, number_of_parameters):
        player = game.player
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            if number_of_parameters == 0:
                print(MSG0.format(command_word=command_word))
            else:
                print(MSG1.format(command_word=command_word))
            return False
        # Si juste "look" -> examiner la pièce
        if number_of_parameters == 0:
            print(player.current_room.get_long_description())
            return True
        else:  # Si "look <objet>" -> examiner l'objet
            obj_name = list_of_words[1]
            obj = next((i for i in player.current_room.inventory if i.name.lower() == obj_name.lower()), None)
            if obj:
                print(f"{obj.name} : {obj.description}")
                return True
            else:
                print(f"\nIl n'y a pas d'objet nommé '{obj_name}' ici.\n")
                return False

    def take(game, list_of_words, number_of_parameters):
        if len(list_of_words) != number_of_parameters + 1:
            print(MSG1.format(command_word=list_of_words[0]))
            return False

        obj_name = list_of_words[1]
        room = game.player.current_room
        # Chercher l'objet dans la salle
        obj = next((i for i in room.inventory if i.name.lower() == obj_name.lower()), None)
        if obj is None:
            print(f"\nIl n'y a aucun '{obj_name}' ici.\n")
            return False

        # Ajouter au joueur et retirer de la salle
        game.player.inventory.append(obj)
        room.inventory.remove(obj)
        print(f"\nVous avez pris '{obj.name}'.\n")
        return True

    def drop(game, list_of_words, number_of_parameters):
        if len(list_of_words) != number_of_parameters + 1:
            print(MSG1.format(command_word=list_of_words[0]))
            return False

        obj_name = list_of_words[1]
        # Chercher l'objet dans l'inventaire
        obj = next((i for i in game.player.inventory if i.name.lower() == obj_name.lower()), None)
        if obj is None:
            print(f"\nVous ne possédez aucun '{obj_name}'.\n")
            return False

        # Retirer du joueur et ajouter à la salle
        game.player.inventory.remove(obj)
        game.player.current_room.inventory.append(obj)
        print(f"\nVous avez posé '{obj.name}'.\n")
        return True

    def talk(game, list_of_words, number_of_parameters):
        player = game.player
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            print(MSG1.format(command_word=list_of_words[0]))
            return False
        npc_name = list_of_words[1]
        npc = next((c for c in player.current_room.characters if c.name.lower() == npc_name.lower()), None)
        if npc:
            print(f"\n{npc.description}\n")
            return True
        else:
            print(f"\nIl n'y a personne nommé '{npc_name}' ici.\n")
            return False

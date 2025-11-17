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
        # Si on a juste "look" -> examiner la pièce
        if number_of_parameters == 0:
            print(player.current_room.get_long_description())
            return True
        # Si on a "look <objet>" -> examiner l'objet
        else:
            obj_name = list_of_words[1]
            obj = player.current_room.get_item(obj_name)
            if obj:
                print(f"{obj.name} : {obj.description}")
                return True
            else:
                print(f"\nIl n'y a pas d'objet nommé '{obj_name}' ici.\n")
                return False

    def take(game, list_of_words, number_of_parameters):
        player = game.player
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False
        item_name = list_of_words[1]
        item = player.current_room.get_item(item_name)
        if item:
            player.add_to_inventory(item)
            player.current_room.remove_item(item)
            print(f"\nVous avez pris {item.name}.\n")
            return True
        else:
            print(f"\nIl n'y a pas d'objet nommé '{item_name}' ici.\n")
            return False

    def talk(game, list_of_words, number_of_parameters):
        player = game.player
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False
        npc_name = list_of_words[1]
        npc = player.current_room.get_npc(npc_name)
        if npc:
            print(f"\n{npc.get_msg()}\n")
            return True
        else:
            print(f"\nIl n'y a personne nommé '{npc_name}' ici.\n")
            return False

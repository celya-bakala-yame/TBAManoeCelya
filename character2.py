# character.py
class Character:
    def __init__(self, name, description, current_room=None, msgs=None):
        self.name = name
        self.description = description
        self.current_room = current_room
        self.msgs = msgs if msgs is not None else ["..."]

    def __str__(self):
        return f"{self.name} : {self.description}"

    def get_msg(self):
        """Retourne cycliquement les messages du personnage"""
        msg = self.msgs.pop(0)
        self.msgs.append(msg)
        return msg

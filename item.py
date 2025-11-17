# item.py

class Item:
    def __init__(self, name, description, weight=0):
        self.name = name
        self.description = description
        self.weight = weight

    def __str__(self):
        return f"{self.name} : {self.description} ({self.weight} kg)"

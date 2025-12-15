class Item:
    def __init__(self, name: str, description: str, weight: float):
        self.name = name
        self.description = description
        self.weight = weight

    def __str__(self):
        return f"{self.name} : {self.description} ({self.weight} kg)"
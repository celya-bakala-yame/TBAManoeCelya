# This file contains the Command class.

class Command:
    """
    This class represents a command. A command is composed of :
    - a command word (ex: 'go', 'look', 'take', 'talk'),
    - a help string,
    - an action function to execute,
    - a number of parameters.

    Attributes:
        command_word (str): The command word.
        help_string (str): The help string describing the command.
        action (function): The action executed when calling the command.
        number_of_parameters (int): Number of parameters expected.

    """

    def __init__(self, command_word, help_string, action, number_of_parameters):
        self.command_word = command_word
        self.help_string = help_string
        self.action = action
        self.number_of_parameters = number_of_parameters
    
    def __str__(self):
        return f"{self.command_word} : {self.help_string}"

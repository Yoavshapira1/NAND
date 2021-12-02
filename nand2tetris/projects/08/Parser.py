"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing

ARITHMETIC_LOGIC_COMMAND = ("add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not", "shiftleft", "shiftright")
BRANCHING = ("label", "if-goto", "goto")
PUSH = "push"
POP = "pop"
FUNCTION = "function"
RETURN = "return"
CALL = "call"

class Parser:
    """
    Handles the parsing of a single .vm file, and encapsulates access to the
    input code. It reads VM commands, parses them, and provides convenient 
    access to their components. 
    In addition, it removes all white space and comments.
    """

    def __init__(self, input_file: typing.TextIO) -> None:
        """Gets ready to parse the input file.

        Args:
            input_file (typing.TextIO): input file.
        """
        self.input_lines = input_file.read().splitlines()
        self.current_line_index = 0
        self.num_of_lines = len(self.input_lines)
        self.current_command = self.input_lines[self.current_line_index]

    def has_more_commands(self) -> bool:
        """Are there more commands in the input?

        Returns:
            bool: True if there are more commands, False otherwise.
        """
        return self.current_line_index < self.num_of_lines

    def advance(self) -> None:
        """Reads the next command from the input and makes it the current 
        command. Should be called only if has_more_commands() is true. Initially
        there is no current command.
        """
        self.current_line_index += 1
        self.current_command = self.input_lines[self.current_line_index] if self.has_more_commands() else None

    def command_type(self) -> str:
        """
        Returns:
            str: the type of the current VM command.
            "C_ARITHMETIC" is returned for all arithmetic commands.
            For other commands, can return:
            "C_PUSH", "C_POP", "C_LABEL", "C_GOTO", "C_IF", "C_FUNCTION",
            "C_RETURN", "C_CALL".
        """
        if self.current_command.startswith("//") or not self.current_command.strip():
            return ""
        elif self.current_command.startswith(ARITHMETIC_LOGIC_COMMAND):
            return "C_ARITHMETIC"
        elif self.current_command.startswith(PUSH):
            return "C_PUSH"
        elif self.current_command.startswith(POP):
            return "C_POP"
        elif self.current_command.startswith(BRANCHING):
            return "C_BRANCHING"
        elif self.current_command.startswith(FUNCTION):
            return "C_FUNCTION"
        elif self.current_command.startswith(RETURN):
            return "C_RETURN"
        elif self.current_command.startswith(CALL):
            return "C_CALL"
        return ""

    def arg1(self) -> str:
        """
        Returns:
            str: the first argument of the current command. In case of 
            "C_ARITHMETIC", the command itself (add, sub, etc.) is returned. 
            Should not be called if the current command is "C_RETURN".
        """
        splited_command = self.current_command.split()
        if self.command_type() == "C_ARITHMETIC":
            return splited_command[0]
        else:
            return splited_command[1]

    def arg2(self) -> int:
        """
        Returns:
            int: the second argument of the current command. Should be
            called only if the current command is "C_PUSH", "C_POP", 
            "C_FUNCTION" or "C_CALL".
        """
        splited_command = self.current_command.split()
        return int(splited_command[2])

    def loop_labels(self):
        """
        Returns:
            str: the label argument of the current command. Should be
            called only if the current command is "C_BRANCHING"
        """
        splited_command = self.current_command.split()
        return splited_command[0], splited_command[1]

    def func_args(self):
        """
        Returns:
            str: the arguments of the current command. Should be
            called only if the current command is "C_FUNCTION" or "C_CALL"
        """
        splited_command = self.current_command.split()
        return splited_command[1], int(splited_command[2])
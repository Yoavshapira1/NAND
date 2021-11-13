"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
import re


class Parser:
    """Encapsulates access to the input code. Reads and assembly language 
    command, parses it, and provides convenient access to the commands 
    components (fields and symbols). In addition, removes all white space and 
    comments.
    """

    def __init__(self, input_file: typing.TextIO) -> None:
        """Opens the input file and gets ready to parse it.

        Args:
            input_file (typing.TextIO): input file.
        """
        self.__lines = []      # List of all lines and their commands
        self.__curLine = 0     # Initialize the line reader 'buffer'
        self.initialize_lines(input_file)

    def initialize_lines(self, input_file: typing.TextIO) -> None:
        """
        Initialize the {line : commands} dictionary
        """
        input_lines = input_file.read().splitlines()
        for line in input_lines:
            l = (line.strip()).split("//")[0]
            if not l == "":
                self.__lines.append(re.sub("\s+","",l))

    def has_more_commands(self) -> bool:
        """Are there more commands in the input?

        Returns:
            bool: True if there are more commands, False otherwise.
        """
        return len(self.__lines) > self.__curLine

    def delete(self) -> None:
        """
        Delete the current line from the parser lines
        Should only be called if commandType() is "L_COMMAND"
        """
        self.__lines.remove(self.__lines[self.__curLine])

    def advance(self) -> None:
        """Reads the next command from the input and makes it the current command.
        Should be called only if has_more_commands() is true.
        """
        self.__curLine += 1

    def reset(self) -> None:
        """
        Reset the line reader and return None
        """
        self.__curLine = 0

    def command_type(self) -> str:
        """
        Returns:
            str: the type of the current command:
            "A_COMMAND" for @Xxx where Xxx is either a symbol or a decimal number
            "C_COMMAND" for dest=comp;jump
            "L_COMMAND" (actually, pseudo-command) for (Xxx) where Xxx is a symbol
        """
        current = self.__lines[self.__curLine]
        if current.startswith("@"):
            return "A_COMMAND"
        elif current.startswith("("):
            return "L_COMMAND"
        elif current == "":
            return ""
        else:
            return "C_COMMAND"

    def symbol(self) -> str:
        """
        Returns:
            str: the symbol or decimal Xxx of the current command @Xxx or
            (Xxx). Should be called only when command_type() is "A_COMMAND" or 
            "L_COMMAND".
        """
        if self.command_type() == "A_COMMAND":
            return self.__lines[self.__curLine].replace("@", "")
        if self.command_type() == "L_COMMAND":
            return self.__lines[self.__curLine].replace("(", "").replace(")", "")

    def split_c_instruction(self):
        """
        Split the C_COMMAND line into components
        """
        dest_split = self.__lines[self.__curLine].split("=")
        dest, comp = (dest_split[0],dest_split[1]) if len(dest_split) == 2\
            else ("",dest_split[0])
        comp_split = comp.split(";")
        comp, jump = (comp_split[0],comp_split[1]) if len(comp_split) == 2 \
            else (comp_split[0],"")
        return dest, comp, jump

    def dest(self) -> str:
        """
        Returns:
            str: the dest mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        return self.split_c_instruction()[0]

    def comp(self) -> str:
        """
        Returns:
            str: the comp mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        return self.split_c_instruction()[1]

    def jump(self) -> str:
        """
        Returns:
            str: the jump mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        return self.split_c_instruction()[2]

"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""

COMP_DICT = {
    "0" : "0101010",
    "1" : "0111111",
    "-1" : "0111010",
    "D" : "0001100",
    "A" : "0110000",
    "M" : "1110000",
    "!D" : "0001101",
    "!A" : "0110001",
    "!M" : "1110001",
    "-D" : "1001111",
    "-A" : "1110011",
    "D+1" : "0011111",
    "A+1" : "0110111",
    "M+1" : "1110111",
    "D-1" : "0001110",
    "A-1" : "0110010",
    "M-1" : "1110010",
    "D+A" : "0000010",
    "D+M" : "1000010",
    "D-A" : "0010011",
    "D-M" : "1010011",
    "A-D" : "0000111",
    "M-D" : "1000111",
    "D&A" : "0000000",
    "D&M" : "1000000",
    "D|A" : "0010101",
    "D|M" : "1010101"
}

JMP_DICT = {
    "" : "000",
    "JGT" : "001",
    "JEQ" : "010",
    "JGE" : "011",
    "JLT" : "100",
    "JNE" : "101",
    "JLE" : "110",
    "JMP" : "111"
}

DEST_DICT = {
    "" : "000",
    "M" : "001",
    "D" : "010",
    "MD" : "011",
    "A" : "100",
    "AM" : "101",
    "AD" : "110",
    "AMD" : "111"
}

class Code:
    """Translates Hack assembly language mnemonics into binary codes."""

    @staticmethod
    def get_c_instruction(parser) -> str:
        """
        Return a string holds for the binary representation of a given parser
        according to a given symbols table.
        Should be called only if parser.commandType() == "C_COMMAND"
        """
        code = "111"
        code += Code.comp(parser.comp())
        code += Code.dest(parser.dest())
        code += Code.jump(parser.jump())
        return code

    @staticmethod
    def get_binary_address(address : int) -> str:
        """
        Return a string holds for the binary representation of a given parser
        according to a given symbols table.
        Should be called iff parser.commandType() == "A_COMMAND"
        """
        return "0" + "{0:015b}".format(address)

    @staticmethod
    def dest(mnemonic: str) -> str:
        """
        Args:
            mnemonic (str): a dest mnemonic string.

        Returns:
            str: 3-bit long binary code of the given mnemonic.
        """
        return DEST_DICT.get(mnemonic)


    @staticmethod
    def comp(mnemonic: str) -> str:
        """
        Args:
            mnemonic (str): a comp mnemonic string.

        Returns:
            str: 7-bit long binary code of the given mnemonic.
        """
        return COMP_DICT.get(mnemonic)


    @staticmethod
    def jump(mnemonic: str) -> str:
        """
        Args:
            mnemonic (str): a jump mnemonic string.

        Returns:
            str: 3-bit long binary code of the given mnemonic.
        """
        return JMP_DICT.get(mnemonic)

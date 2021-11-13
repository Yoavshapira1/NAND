"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing

ARITHMETIC = {"add": "@SP\nAM=M-1\nD=M\nA=A-1\nM=D+M\n",
              "sub": "@SP\nAM=M-1\nD=M\nA=A-1\nM=D-M\n",
              "neg": "@SP\nA=M\nA=A-1\nM=-M\n",
              "eq": "@SP\nAM=M-1\nD=M\n@R13\nM=D\nA=A-1\nD=M\nM=0\n@R14\nM=D\n@X_neg{index}\nR14;GLT\n@CONTINUE{index}\n"
                    "  R13;JLT\n   @R14\n  D=M\n   @R13\n  M=M-D\n   "
                    "@PRE_CON{index}\n   0;JMP\n"
                    "(X_neg{index})\n   @CONTINUE{index}\n  R13;JGT\n   @R14\n  D=M\n   @R13\n  M=M-D\n   "
                    "@PRE_CON{index}\n   0;JMP\n"
                    ""
                    "D=D-M\nM=0\n@TRUE{index}\n "
                    " D;JEQ\n(TRUE{index})\n  @SP\n   A=M-1\n   M=-1\n  @CONTINUE{index}\n  0;JMP\n(CONTINUE{index})\n",
              "gt": "@SP\nAM=M-1\nD=M\nA=A-1\nD=D-M\nM=0\n@TRUE{index}\n "
                    " D;JLT\n(TRUE{index})\n  @SP\n   A=M-1\n   M=-1\n  @CONTINUE{index}\n  0;JMP\n(CONTINUE{index})\n",
              "lt": "@SP\nAM=M-1\nD=M\nA=A-1\nD=D-M\nM=0\n@TRUE{index}\n "
                    " D;JGT\n(TRUE{index})\n  @SP\n   A=M-1\n   M=-1\n  @CONTINUE{index}\n  0;JMP\n(CONTINUE{index})\n",
              "and": "@SP\nAM=M-1\nD=M\nA=A-1\nM=D&M\n",
              "or": "@SP\nAM=M-1\nD=M\nA=A-1\nM=D|M\n",
              "not": "@SP\nA=M\nA=A-1\nM=!M\n"}
PUSH = {"constant": "@{index}\nD=A\n@SP\nAM=M+1\nA=A-1\nM=D\n"}




class CodeWriter:
    """Translates VM commands into Hack assembly code."""

    def __init__(self, output_stream: typing.TextIO) -> None:
        """Initializes the CodeWriter.

        Args:
            output_stream (typing.TextIO): output stream.
        """
        self.output_stream = output_stream
        self.general_continue_index = 0

    def set_file_name(self, filename: str) -> None:
        """Informs the code writer that the translation of a new VM file is 
        started.

        Args:
            filename (str): The name of the VM file.
        """
        print("starting translation " + filename)

    def write_arithmetic(self, command: str) -> None:
        """Writes the assembly code that is the translation of the given 
        arithmetic command.

        Args:
            command (str): an arithmetic command.
        """
        self.output_stream.write(ARITHMETIC[command].format(index = self.general_continue_index))
        if command in ["gt", "lt", "eq"]:
            self.general_continue_index += 1

    def write_push_pop(self, command: str, segment: str, index: int) -> None:
        """Writes the assembly code that is the translation of the given 
        command, where command is either C_PUSH or C_POP.

        Args:
            command (str): "C_PUSH" or "C_POP".
            segment (str): the memory segment to operate on.
            index (int): the index in the memory segment.
        """
        if command == "C_PUSH":
            self.output_stream.write(PUSH[segment].format(index=str(index)))

    def write_comment(self, comment: str) -> None:
        """
        write as a comment the next VM command that translated.
        :param comment: the command to write
        :return: None
        """
        self.output_stream.write("//" + comment + "\n")

    def close(self) -> None:
        """Closes the output file."""
        # Your code goes here!
        pass

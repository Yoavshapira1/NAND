"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""

import typing

        ###################### PUSH AND POP ############################

### NOTICE: R15 is used for temporarily keeping the desired
### value to be pushed to stack


SEG = {"constant": "",
       "local": "LCL",
       "argument": "ARG",
       "this": "THIS",
       "that": "THAT",
       "temp": "R5",
       "static": "",
       "pointer": "THIS"}

# SEGMENTS = ["SP", "LCL", "ARG", "THIS", "THAT"]
# BASES = [256, 1000, 2000, 3000, 4000]
# SEGMENTS_POINTERS =[0,1,2,3,4,5]

INIT_SP = "@256\nD=A\n@SP\nM=D\n"
KEEP_ADDR = "@R15\nM=D\n"
GET_ADDR = "@{index}\nD=A\n@{segment}\nD=M+D\n"
GET_POINTER_OR_TEMP_ADDR = "@{index}\nD=A\n@{segment}\nD=A+D\n"
SAVE_ADDR = GET_ADDR + KEEP_ADDR
SAVE_POINTER_OR_TEMP_ADDR = GET_POINTER_OR_TEMP_ADDR + KEEP_ADDR
DATA_TO_STACK = "@SP\nAM=M+1\nA=A-1\nM=D\n"
DATA_TO_ADDR = "@R15\nA=M\nM=D\n"
STACK_TO_DATA = "@SP\nAM=M-1\nD=M\n"
NEW_STATIC = "@{static}\nM=D\n"
STATIC_TO_DATA = "@{static}\nD=M\n"
SEG_TO_DATA = "@{index}\nD=A\n@{segment}\nA=M+D\nD=M\n"
POINTER_OR_TEMP_TO_DATA = "@{index}\nD=A\n@{segment}\nA=A+D\nD=M\n"
CONST_TO_DATA = "@{index}\nD=A\n"
VALUE_TO_TEMP = "@{segment}\nD=M\n@R13\nM=D\n"
RET_ADDRESS = "@R13\nD=M\n@5\nD=D-A\n@R14\nM=D\n"
SP_RET_UPDATE = "@{segment}\nD=M\nD=D+1\n@SP\nM=D\n"
UPDATE_SEGS = "@R13\nD=M\n@{index}\nD=D-A\nA=D\nD=M\n@{segment}\nM=D\n"
PUSH_SEG_ADDRESS = "@{segment}\nD=M\n" + DATA_TO_STACK
RETURN_LABEL = "@{label}\nD=A\n" + DATA_TO_STACK


UPDATE_THAT = UPDATE_SEGS.format(index=1, segment=SEG["that"])
UPDATE_THIS = UPDATE_SEGS.format(index=2, segment=SEG["this"])
UPDATE_ARG = UPDATE_SEGS.format(index=3, segment=SEG["argument"])
UPDATE_LCL = UPDATE_SEGS.format(index=4, segment=SEG["local"])
REPOSITION_ARG = "@5\nD=A\n@SP\nD=M-D\n@{nArgs}\nD=D-A\n@ARG\nM=D\n"
REPOSITION_LCL = "@SP\nD=M\n@LCL\nM=D\n"

PUSH = {
    "constant": CONST_TO_DATA + DATA_TO_STACK,
    "local": SEG_TO_DATA + DATA_TO_STACK,
    "argument": SEG_TO_DATA + DATA_TO_STACK,
    "this": SEG_TO_DATA + DATA_TO_STACK,
    "that": SEG_TO_DATA + DATA_TO_STACK,
    "temp": POINTER_OR_TEMP_TO_DATA + DATA_TO_STACK,
    "pointer": POINTER_OR_TEMP_TO_DATA + DATA_TO_STACK,
    "static": STATIC_TO_DATA + DATA_TO_STACK
}

POP = {
    "constant": CONST_TO_DATA + STACK_TO_DATA + DATA_TO_ADDR,
    "local": SAVE_ADDR + STACK_TO_DATA + DATA_TO_ADDR,
    "argument": SAVE_ADDR + STACK_TO_DATA + DATA_TO_ADDR,
    "this": SAVE_ADDR + STACK_TO_DATA + DATA_TO_ADDR,
    "that": SAVE_ADDR + STACK_TO_DATA + DATA_TO_ADDR,
    "temp": SAVE_POINTER_OR_TEMP_ADDR + STACK_TO_DATA + DATA_TO_ADDR,
    "pointer": SAVE_POINTER_OR_TEMP_ADDR + STACK_TO_DATA + DATA_TO_ADDR,
    "static": STACK_TO_DATA + NEW_STATIC
}

       ########################### BRANCHING ##############################

NEW_LABEL = "({label})\n"
GOTO = "@{label}\n0;JMP\n"
IF_GOTO = STACK_TO_DATA + "@{label}\nD;JGT\n"
FUNCTION = "({label})\n"
GOTO_RET_ADD = "@R14\nA=M\n0;JMP\n"


BRANCHING = {
            "label": NEW_LABEL,
            "goto": GOTO,
            "if-goto": IF_GOTO
            }

END = "(END)\n@END\n0;JMP"

    ########################### ARITHMETIC ##############################

ARITHMETIC = {"add": "@SP\nAM=M-1\nD=M\nA=A-1\nM=D+M\n",
              "sub": "@SP\nAM=M-1\nD=M\nA=A-1\nM=M-D\n",
              "neg": "@SP\nA=M\nA=A-1\nM=-M\n",
              "eq": "@SP\nAM=M-1\nD=M\n@R13\nM=D\n@SP\nA=M-1\nD=M\nM=0\n@R14\nM=D\n@R14\nD=M\n@X_POS{index}\nD;JGT\n"
                    "@R13\nD=M\n@END{index}\nD;JGT\n@CHECK{index}\n0;JMP\n(X_POS{index})\n   @R13\n  D=M\n   @END{index}"
                    "\n   D;JLT\n(CHECK{index})\n   @R14\n   D=M\n   @R13\n    M=M-D\n   @R13\n    D=M\n   @TRUE{index}"
                    "\n   D;JEQ\n   @END{index}\n    0;JMP\n(TRUE{index})\n    @SP\n    A=M-1\n    M=-1\n   @END{index}\n"
                    "   0;JMP\n(END{index})\n",
              "gt": "@SP\nAM=M-1\nD=M\n@R13\nM=D\n@SP\nA=M-1\nD=M\nM=0\n@R14\nM=D\n@R14\nD=M\n@X_POS{index}\nD;JGT\n"
                    "@R13\nD=M\n@END{index}\nD;JGT\n@CHECK{index}\n0;JMP\n(X_POS{index})\n   @R13\n  D=M\n   @TRUE{index}"
                    "\n   D;JLT\n(CHECK{index})\n   @R14\n   D=M\n   @R13\n    M=D-M\n   @R13\n    D=M\n   @TRUE{index}"
                    "\n   D;JGT\n   @END{index}\n    0;JMP\n(TRUE{index})\n    @SP\n    A=M-1\n    M=-1\n    @END{index}\n"
                    "   0;JMP\n(END{index})\n",
              "lt": "@SP\nAM=M-1\nD=M\n@R13\nM=D\n@SP\nA=M-1\nD=M\nM=0\n@R14\nM=D\n@R14\nD=M\n@X_POS{index}\nD;JGT\n"
                    "@R13\nD=M\n@END{index}\nD;JGT\n@CHECK{index}\n0;JMP\n(X_POS{index})\n   @R13\n  D=M\n   @END{index}"
                    "\n   D;JLT\n(CHECK{index})\n   @R14\n   D=M\n   @R13\n    M=D-M\n   @R13\n    D=M\n   @TRUE{index}"
                    "\n   D;JLT\n   @END{index}\n    0;JMP\n(TRUE{index})\n    @SP\n    A=M-1\n    M=-1\n    @END{index}\n"
                    "   0;JMP\n(END{index})\n",
              "and": "@SP\nAM=M-1\nD=M\nA=A-1\nM=D&M\n",
              "or": "@SP\nAM=M-1\nD=M\nA=A-1\nM=D|M\n",
              "not": "@SP\nA=M\nA=A-1\nM=!M\n",
              "shiftleft": "@SP\nA=M\nA=A-1\nM=M<<\n",
              "shiftright": "@SP\nA=M\nA=A-1\nM=M>>\n"}


class CodeWriter:
    """Translates VM commands into Hack assembly code."""

    def __init__(self, output_stream: typing.TextIO) -> None:
        """Initializes the CodeWriter.

        Args:
            output_stream (typing.TextIO): output stream.
        """
        self.output_stream = output_stream
        self.filename = ""
        self.cur_function = ""
        self.general_continue_index = 0
        self.return_counter = 0

    def set_file_name(self, filename: str) -> None:
        """Informs the code writer that the translation of a new VM file is 
        started.

        Args:
            filename (str): The name of the VM file.
        """
        self.filename = filename

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
            self.output_stream.write(PUSH[segment].format(
                index=str(index), segment=SEG[segment],
                static=self.filename+".{}".format(index)))
        if command == "C_POP":
            self.output_stream.write(POP[segment].format(
                index=str(index), segment=SEG[segment],
                static=self.filename+".{}".format(index)))

    def write_branching(self, command: str, label: str) -> None:
        """Writes the assembly code that is the translation of the given
        command, where command is of kind "C_BRANCHING"

        Args:
            command (str): "label", "goto", or "if-goto"
            label (str): the label of the loop to jump to, if needed
        """
        label_name = self.cur_function + "$" + label
        self.output_stream.write(BRANCHING[command].format(label=label_name))

    def write_comment(self, comment: str) -> None:
        """
        write as a comment the next VM command that translated.
        :param comment: the command to write
        :return: None
        """
        self.output_stream.write("//" + comment + "\n")

    def write_init(self):
        """
        Writes the assembly code that effects the
        VM initialization (also called bootstrap
        code). This code should be placed in the
        ROM beginning in address 0x0000.
        """
        # for base, segment in zip(BASES, SEGMENTS):
        self.output_stream.write(INIT_SP)
        self.write_call("Sys.init", 0)

    def write_function(self, function_mame: str, num_vals: int) -> None:
        """Writes the assembly code that is the translation of the given
        command, where command is of kind "C_FUNCTION"

        Args:
            function_mame (str): the name of the function.
            num_vals (int): the number of local variables for the function.
        """
        self.output_stream.write(FUNCTION.format(label=function_mame))
        for i in range(num_vals):
            self.output_stream.write(PUSH["constant"].format(index=0))
        self.cur_function = function_mame

    def write_call(self, function_mame: str, num_args: int) -> None:
        """
        Writes a call function code
        """
        returnAddress = "{function}$ret.{index}".format(function=self.cur_function, index=self.return_counter)
        self.return_counter += 1
        self.output_stream.write(RETURN_LABEL.format(label=returnAddress))
        self.output_stream.write(PUSH_SEG_ADDRESS.format(segment="LCL"))
        self.output_stream.write(PUSH_SEG_ADDRESS.format(segment="ARG"))
        self.output_stream.write(PUSH_SEG_ADDRESS.format(segment="THIS"))
        self.output_stream.write(PUSH_SEG_ADDRESS.format(segment="THAT"))
        self.output_stream.write(REPOSITION_ARG.format(nArgs=str(num_args)))
        self.output_stream.write(REPOSITION_LCL)
        self.output_stream.write(BRANCHING["goto"].format(label=function_mame))
        self.output_stream.write(BRANCHING["label"].format(label=returnAddress))


    def write_return(self) -> None:
        """Writes the assembly code that is the translation of the return command.
        """
        self.output_stream.write(VALUE_TO_TEMP.format(segment=SEG["local"]))
        self.output_stream.write(RET_ADDRESS)
        self.output_stream.write(POP["argument"].format(index=0, segment=SEG["argument"]))
        self.output_stream.write(SP_RET_UPDATE.format(segment=SEG["argument"]))
        self.output_stream.write(UPDATE_THAT)
        self.output_stream.write(UPDATE_THIS)
        self.output_stream.write(UPDATE_ARG)
        self.output_stream.write(UPDATE_LCL)
        self.output_stream.write(GOTO_RET_ADD)

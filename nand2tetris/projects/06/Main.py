"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import os
import sys
import typing
from SymbolTable import SymbolTable
from Parser import Parser
from Code import Code


def read_loops(parser : Parser, symbols : SymbolTable) -> None:
    """
    Read the Loops symbols in a parser object and write them to corresponds
    SymbolTable object
    """
    line = 0
    while parser.has_more_commands():   # First read LOOP symbols
        if parser.command_type() == "L_COMMAND":
            symbols.add_entry(parser.symbol(), line)
            parser.delete()
        else:
            line += 1
            parser.advance()
    parser.reset()

def write_code(parser : Parser, symbols : SymbolTable,
               output_file: typing.TextIO) -> None:
    """
    Write the code for a given parser and a corresponds symbols table, to the
    gievn path of output file
    """
    n = 16
    while parser.has_more_commands():   # Than read commands
        if parser.command_type() == "A_COMMAND":
            sym = parser.symbol()
            if not sym.isdigit():     # instruction doesnt contain a symbol
                if symbols.contains(sym):    # check if already handled
                    code = "0" + "{0:015b}".format(symbols.get_address(sym))
                else:
                    symbols.add_entry(sym, n)
                    code = "0" + "{0:015b}".format(n)
                    n += 1
            else:   # if it is a number, just write it into a binary
                code = "0" + "{0:015b}".format(int(sym))
            output_file.write(code+"\n")

        elif (parser.command_type() == "C_COMMAND"):
            code = Code.get_c_instruction(parser)
            output_file.write(code+"\n")
        parser.advance()

def assemble_file(
        input_file: typing.TextIO, output_file: typing.TextIO) -> None:
    """Assembles a single file.

    Args:
        input_file (typing.TextIO): the file to assemble.
        output_file (typing.TextIO): writes all output to this file.
    """
    symbols = SymbolTable()             # Symbols Table Initialization
    parser = Parser(input_file)         # Parser Object
    read_loops(parser, symbols)         # First reads the loops
    write_code(parser, symbols, output_file)    # Write the binary code

if "__main__" == __name__:
    # Parses the input path and calls assemble_file on each input file
    if not len(sys.argv) == 2:
        sys.exit("Invalid usage, please use: Assembler <input path>")
    argument_path = os.path.abspath(sys.argv[1])
    if os.path.isdir(argument_path):
        files_to_assemble = [
            os.path.join(argument_path, filename)
            for filename in os.listdir(argument_path)]
    else:
        files_to_assemble = [argument_path]
    for input_path in files_to_assemble:
        filename, extension = os.path.splitext(input_path)
        if extension.lower() != ".asm":
            continue
        output_path = filename + ".hack"
        with open(input_path, 'r') as input_file, \
                open(output_path, 'w') as output_file:
            assemble_file(input_file, output_file)

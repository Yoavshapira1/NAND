"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import glob
import os
import sys
import typing
from Parser import Parser
from CodeWriter import CodeWriter

FLAG_INIT = False

def run_through_vm_code(parser, code_write):
    while parser.has_more_commands():
        command_type = parser.command_type()
        if not command_type:
            parser.advance()
            continue

        code_write.write_comment(parser.input_lines[parser.current_line_index])
        if command_type == "C_ARITHMETIC":
            code_write.write_arithmetic(parser.arg1())
        elif command_type == "C_PUSH" or command_type == "C_POP":
            code_write.write_push_pop(command_type, parser.arg1(), parser.arg2())
        elif command_type == "C_BRANCHING":
            code_write.write_branching(*parser.loop_labels())
        elif command_type == "C_FUNCTION":
            code_write.write_function(*parser.func_args())
        elif command_type == "C_CALL":
            code_write.write_call(*parser.func_args())
        elif command_type == "C_RETURN":
            code_write.write_return()
        parser.advance()


def translate_file(input_file: typing.TextIO, output_file: typing.TextIO) -> None:
    """Translates a single file.

    Args:
        input_file (typing.TextIO): the file to translate.
        output_file (typing.TextIO): writes all output to this file.
    """
    global FLAG_INIT
    input_filename, input_extension = os.path.splitext(os.path.basename(input_file.name))
    code_writer = CodeWriter(output_file)   # Write the hack code
    if not FLAG_INIT:
        code_writer.write_init()
        FLAG_INIT = True
    parser = Parser(input_file)  # Parser Object
    code_writer.set_file_name(input_filename)
    run_through_vm_code(parser, code_writer)

if "__main__" == __name__:
    # Parses the input path and calls translate_file on each input file
    if not len(sys.argv) == 2:
        sys.exit("Invalid usage, please use: VMtranslator <input path>")
    argument_path = os.path.abspath(sys.argv[1])
    if os.path.isdir(argument_path):
        files_to_translate = [
            os.path.join(argument_path, filename)
            for filename in os.listdir(argument_path)]
        output_path = os.path.join(argument_path, os.path.basename(
            argument_path))
    else:
        files_to_translate = [argument_path]
        output_path, extension = os.path.splitext(argument_path)
    output_path += ".asm"
    with open(output_path, 'w') as output_file:
        for input_path in files_to_translate:
            filename, extension = os.path.splitext(input_path)
            if extension.lower() != ".vm":
                continue
            with open(input_path, 'r') as input_file:
                translate_file(input_file, output_file)

"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
import Grammer
import re

STRING = "STRING"


class JackTokenizer:
    """Removes all comments from the input stream and breaks it
    into Jack language tokens, as specified by the Jack grammar.
    """

    def __init__(self, input_stream: typing.TextIO) -> None:
        """Opens the input stream and gets ready to tokenize it.

        Args:
            input_stream (typing.TextIO): input stream.
        """
        self.clean_code = ""
        self.all_strings = []
        self.string_index = 0
        self.cur_token = ""
        self.cur_token_type = None
        self.first_process(input_stream.read().splitlines())

    def first_process(self, lines):
        """
        remove all comment empty lines more then one whitespace from the input file and make
        one long string to deal with later.
        in addition, all string replace with STRING and keep them in a different array which is data member.
        :param lines: the lines of the file.
        """
        num_of_lines = len(lines)
        lines.append("")
        index = 0
        cur_line = lines[index]
        while index < num_of_lines:
            string_i = cur_line.find("\"")
            comment_doc_i = cur_line.find("/*")
            comment_i = cur_line.find("//")
            if re.match(r'\s*//', cur_line) or cur_line == "":  #deal with regular comment or empty line
                index += 1
                cur_line = lines[index]
            elif string_i != -1: # deal with string
                if (comment_doc_i != -1 and string_i < comment_doc_i) or comment_doc_i == -1:
                    parts = cur_line.split("\"")
                    self.clean_code += re.sub('\s+', ' ', parts[0])
                    self.clean_code += Grammer.STRING
                    self.all_strings.append(parts[1])
                    cur_line = ''.join(parts[2:])
                    continue
            elif comment_doc_i != -1: # deal with documentation comment
                parts = cur_line.split("/*")
                self.clean_code += re.sub('\s+', ' ', parts[0])
                cur_line = ''.join(parts[1:])
                while True:
                    temp = cur_line.split("*/")
                    if len(temp) == 1:
                        index += 1
                        cur_line = lines[index]
                    else:
                        cur_line = ''.join(temp[1:])
                        break
            elif comment_i != -1: # deal with regular comment in a middle of line
                parts = cur_line.split("//")
                self.clean_code += re.sub('\s+', ' ', parts[0])
                index += 1
                cur_line = lines[index]
            else: # regular line
                self.clean_code += re.sub('\s+', ' ', cur_line)
                index += 1
                cur_line = lines[index]
        self.clean_code = self.clean_code.rstrip()

    def has_more_tokens(self) -> bool:
        """Do we have more tokens in the input?

        Returns:
            bool: True if there are more tokens, False otherwise.
        """
        return len(self.clean_code) > 0

    def advance(self) -> None:
        """Gets the next token from the input and makes it the current token. 
        This method should be called if has_more_tokens() is true. 
        Initially there is no current token.
        """
        if self.cur_token_type == Grammer.STRING_CONSTANT:
            self.string_index += 1
        for token_reg in Grammer.TOKEN_TYPES_REGEX.keys():
            token = re.match("\s*" + token_reg, self.clean_code)
            if token:
                self.cur_token = re.sub('\s+', '', token.group())
                self.cur_token_type = Grammer.TOKEN_TYPES_REGEX[token_reg]
                self.clean_code = self.clean_code[len(token.group()):]
                break

    def token_type(self) -> str:
        """
        Returns:
            str: the type of the current token, can be
            "KEYWORD", "SYMBOL", "IDENTIFIER", "INT_CONST", "STRING_CONST"
        """
        return self.cur_token_type

    def get_token(self):
        if self.cur_token_type == Grammer.STRING_CONSTANT:
            return self.all_strings[self.string_index]
        return self.cur_token

"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
from JackTokenizer import JackTokenizer


class CompilationEngine:
    """Gets input from a JackTokenizer and emits its parsed structure into an
    output stream.
    """

    def __init__(self, input_stream: JackTokenizer,
                output_stream: typing.TextIO) -> None:
        """
        Creates a new compilation engine with the given input and output. The
        next routine called must be compileClass()
        :param input_stream: The input stream.
        :param output_stream: The output stream.
        """
        self.tokenizer = input_stream
        self.output_stream = output_stream
        self.cur_token = ""
        pass

    def print_to_output(self):
        type = self.tokenizer.cur_token_type
        token = self.tokenizer.cur_token
        self.output_stream.write(' {} </{}\n>'.format(type, token, type))

    def compile(self, expectation):
        self.tokenizer.advance()
        token_type = self.tokenizer.token_type()
        if token_type != expectation:
            raise Exception()
        self.output_stream.write('<{}>'.format(token_type))
        self.compile()
        self.output_stream.write('<{}>'.format(token_type))



    def compile_class(self) -> None:
        """Compiles a complete class."""
        RULE = [IDENTIFIER, '{', CLASS_VAR_DEC, SUBROUTINE_DEC, '}']
        self.output_stream.write('<class>')
        self.output_stream.write('<keyword>{}</keyword>').format(CLASS)
        for rule in RULE:

        self.output_stream.write('</class>')


    def compile_class_var_dec(self) -> None:
        """Compiles a static declaration or a field declaration."""
        # Your code goes here!
        pass

    def compile_subroutine(self) -> None:
        """Compiles a complete method, function, or constructor."""
        # Your code goes here!
        pass

    def compile_parameter_list(self) -> None:
        """Compiles a (possibly empty) parameter list, not including the 
        enclosing "()".
        """
        # Your code goes here!
        pass

    def compile_var_dec(self) -> None:
        """Compiles a var declaration."""
        # Your code goes here!
        pass

    def compile_statements(self) -> None:
        """Compiles a sequence of statements, not including the enclosing 
        "{}".
        """
        # Your code goes here!
        pass

    def compile_do(self) -> None:
        """Compiles a do statement."""
        # Your code goes here!
        pass

    def compile_let(self) -> None:
        """Compiles a let statement."""
        # Your code goes here!
        pass

    def compile_while(self) -> None:
        """Compiles a while statement."""
        RULE = [WHILE, '(', EXPRESSION, ')', '{', STATEMENTS, '}']
        self.output_stream.write("<whileStatement>\n")
        for rule in RULE:
            # advance the tokenizer
            # get the token's type
            # if type != rule, raise exception
            # else: print <type>___</type\n>
            #       compile_type

            self.tokenizer.advance()
            token_type = self.token.token_type()
            if token_type != rule:
                raise Exception()
            print('<type> {} </type\n>'.format(token_type))
            compile('shallow', )
        self.output_stream.write("</whileStatement>\n")

    def compile_return(self) -> None:
        """Compiles a return statement."""
        pass

    def compile_if(self) -> None:
        """Compiles a if statement, possibly with a trailing else clause."""
        # Your code goes here!
        pass

    def compile_expression(self) -> None:
        """Compiles an expression."""
        # Your code goes here!
        pass

    def compile_term(self) -> None:
        """Compiles a term. 
        This routine is faced with a slight difficulty when
        trying to decide between some of the alternative parsing rules.
        Specifically, if the current token is an identifier, the routing must
        distinguish between a variable, an array entry, and a subroutine call.
        A single look-ahead token, which may be one of "[", "(", or "." suffices
        to distinguish between the three possibilities. Any other token is not
        part of this term and should not be advanced over.
        """
        # Your code goes here!
        pass

    def compile_expression_list(self) -> None:
        """Compiles a (possibly empty) comma-separated list of expressions."""
        # Your code goes here!
        pass

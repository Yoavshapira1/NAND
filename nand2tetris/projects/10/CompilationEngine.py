"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
from JackTokenizer import JackTokenizer

TERMINALS = ["keyword", "identifier", "integerConstant", "stringConstant", "symbol"]
NON_TERMINALS = ["class", "classVarDec","subroutineDec", "parameterList",
                 "subroutineBody", "varDec", "statements", "LetStatement",
                 "ifStatement", "whileStatement", "doStatement", "returnStatement",
                 "expression", "term", "expressionList"]

STATEMENTS = ['let', 'while', 'if', 'do', 'return']

# TODO: no compilexxx methods:
#   type, className, subroutineName, variableName, statement, subroutineCall


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


    def print_to_output(self):
        type = self.tokenizer.cur_token_type
        token = self.tokenizer.cur_token
        self.output_stream.write(' {} </{}\n>'.format(type, token, type))

    def write_terminal_element(self):
        """ Output for types: keyword, symbols, constant, identifier"""

        # write <type>
        opening = '<{}>'.format(self.tokenizer.cur_token_type)

        # write <xxx>
        val = ' ' + self.tokenizer.cur_token + ' '

        # write </type>
        closing = '</{}>\n'.format(self.tokenizer.cur_token_type)

        self.output_stream.write(opening + val + closing)

    def non_terminal_output(self):
        """ Output types that are NOT: keyword, symbols, constant, identifier"""

        # write <type>
        self.output_stream.write('<{}>\n'.format(self.tokenizer.cur_token_type))

        # write recursively the content of xxx
        self.compile_recursive()

        # write </type>
        self.output_stream.write('</{}>\n'.format(self.tokenizer.cur_token_type))

    def compile_recursive(self):

        non_terminal_type = self.tokenizer.token_type()
        if (non_terminal_type == CLASS):
            self.compile_class()
        if (non_terminal_type == WHILE):
            self.compile_while()

        self.tokenizer.advance()
        token_type = self.tokenizer.token_type()
        if token_type != expectation:
            raise Exception()
        self.output_stream.write('<{}>'.format(token_type))
        self.compile()
        self.output_stream.write('<{}>'.format(token_type))



    def compile_class(self) -> None:
        """Compiles a complete class."""
        RULE = [CLASS, IDENTIFIER, '{', CLASS_VAR_DEC, SUBROUTINE_DEC, '}']
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
        "{}":
        [doStatement|letStatement|whileStatement|returnStatement|ifStatement]*
        """
        while self.tokenizer.cur_token in STATEMENTS:
            if self.tokenizer.cur_token == 'let':
                self.compile_let()
            elif self.tokenizer.cur_token == 'do':
                self.compile_do()
            elif self.tokenizer.cur_token == 'while':
                self.compile_while()
            elif self.tokenizer.cur_token == 'if':
                self.compile_if()
            elif self.tokenizer.cur_token == 'return':
                self.compile_return()

    def compile_do(self) -> None:
        """Compiles a do statement:
        'do' subroutineCall ';' which become:
        <doStatement>
            <keyword> do </keyword>
            // subroutineCall ...
            <symbol> ; </symbol>
        </doStatement>
        """
        # <doStatement>
        self.output_stream.write("<doStatement>\n")

        # <keyword> do </keyword>
        self.non_terminal_output()
        self.tokenizer.advance()

        # // subroutineCall - recursive
        self.compile_subroutine_call()

        # <symbol> ; </symbol>
        self.non_terminal_output()
        self.tokenizer.advance()

        # </doStatement>
        self.output_stream.write("</doStatement>\n")


    def compile_let(self) -> None:
        """Compiles a let statement:
        'let' varName ['['expression']']? '=' expression ';' which become:
        <letStatement>
            <identifier> varName </identifier>
            // [expression]?...
            <symbol> = </symbol>
            // expression ...
            <symbol> ; </symbol>
        </letStatement>
        """
        # <letStatement>
        self.output_stream.write("<letStatement>\n")

        # <keyword> let </keyword>
        self.non_terminal_output()
        self.tokenizer.advance()

        # <identifier> varName </identifier>
        self.write_terminal_element()
        self.tokenizer.advance()

        if self.tokenizer.cur_token == '[':
            # <symbol> [ </symbol>
            self.write_terminal_element()
            self.tokenizer.advance()

            # // expression - recursive
            self.compile_expression()

            # <symbol> ] </symbol>
            self.write_terminal_element()
            self.tokenizer.advance()

        # <symbol> = </symbol>
        self.write_terminal_element()
        self.tokenizer.advance()

        # // expression - recursive
        self.compile_expression()

        # <symbol> ; </symbol>
        self.write_terminal_element()
        self.tokenizer.advance()

        # </letStatement>
        self.output_stream.write("</letStatement>\n")

    def compile_while(self) -> None:
        """Compiles a while statement:
        'while' '(' expression ')' '{' statements '}' which become:
        <whileStatement>
            <keyword> while </keyword>
            <symbol> ( </symbol>
            // expression ...
            <symbol> ) </symbol>
            <symbol> { </symbol>
            // statements ...
            <symbol> } </symbol>
        </whileStatement>
        """
        # <whileStatement>
        self.output_stream.write("<whileStatement>\n")

        # <keyword> while </keyword>
        self.non_terminal_output()
        self.tokenizer.advance()

        # <symbol> ( </symbol>
        self.write_terminal_element()
        self.tokenizer.advance()

        # // expression - recursive
        self.compile_expression()

        # <symbol> ) </symbol>
        self.write_terminal_element()
        self.tokenizer.advance()

        # <symbol> { </symbol>
        self.write_terminal_element()
        self.tokenizer.advance()

        # // statements - recursive
        self.compile_statements()

        # <symbol> } </symbol>
        self.write_terminal_element()
        self.tokenizer.advance()

        # </whileStatement>
        self.output_stream.write("</whileStatement>\n")

    def compile_return(self) -> None:
        """Compiles a return statement:
        'return' [expression]? ';' which becomes:
        <returnStatement>
            <keyword> return </keyword>
            // expression?
            <symbol> ; </symbol>
        </returnStatement>
        """

        # <returnStatement>
        self.output_stream.write("<returnStatement>\n")

        # <keyword> return </keyword>
        self.write_terminal_element()
        self.tokenizer.advance()

        # // expression? - recursive
        if self.tokenizer.cur_token() != ';':
            self.compile_expression()

        # <symbol> ; </symbol>
        self.write_terminal_element()
        self.tokenizer.advance()

        # </returnStatement>
        self.output_stream.write("</returnStatement>\n")

    def compile_if(self) -> None:
        """Compiles a if statement, possibly with a trailing else clause:
        'if' '(' expression ')' '{' statements '}' [else]? >>>
        <ifStatement>
            <keyword> if </keyword>
            <symbol> ( </symbol>
            // expression ...
            <symbol> ) </symbol>
            <symbol> { </symbol>
            // statements ...
            <symbol> } </symbol>
            // else?
        </ifStatement>
        """

        # <ifStatement>
        self.output_stream.write("<ifStatement>\n")

        # <keyword> if </keyword>
        self.non_terminal_output()
        self.tokenizer.advance()

        # <symbol> ( </symbol>
        self.write_terminal_element()
        self.tokenizer.advance()

        # // expression - recursive
        self.compile_expression()

        # <symbol> ) </symbol>
        self.write_terminal_element()
        self.tokenizer.advance()

        # <symbol> { </symbol>
        self.write_terminal_element()
        self.tokenizer.advance()

        # // statements - recursive
        self.compile_statements()

        # <symbol> } </symbol>
        self.write_terminal_element()
        self.tokenizer.advance()

        # //else?
        if self.tokenizer.cur_token == 'else':
            # <keyword> else </keyword>
            self.write_terminal_element()
            self.tokenizer.advance()

            # <symbol> { </symbol>
            self.write_terminal_element()
            self.tokenizer.advance()

            # // statements - recursive
            self.compile_statements()

            # <symbol> } </symbol>
            self.write_terminal_element()
            self.tokenizer.advance()

        # </ifStatement>
        self.output_stream.write("</ifStatement>\n")


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

    def compile_subroutine_call(self):
        """Compile a subroutineCall.
         subroutineName '(' expressionList ')' |
          (className | varName)'.'subroutineName '(' expressionList '')'
          which becomes:
            [<identifier> mainName </identifier>
            <symbol> '.' </symbol>]?
            <identifier> subName </identifier>
            <symbol> '(' </symbol>
            // expressionList ...
            <symbol> ')' </symbol>
         """
        # <identifier> mainName </identifier>
        self.write_terminal_element()
        self.tokenizer.advance()

        if self.tokenizer.cur_token == '(':
            pass

        else:
            # <symbol> . </symbol>
            self.write_terminal_element()
            self.tokenizer.advance()

            # <identifier> subName </identifier>
            self.write_terminal_element()
            self.tokenizer.advance()

        #<symbol> '(' </symbol>
        self.write_terminal_element()
        self.tokenizer.advance()

        #// expressionList - recursive
        self.compile_expression()


        #<symbol> ')' </symbol>
        self.write_terminal_element()
        self.tokenizer.advance()
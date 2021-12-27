"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
from JackTokenizer import JackTokenizer
from SymbolTable import SymbolTable
from VMWriter import VMWriter
from Grammer import *


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
        self.writer = VMWriter(output_stream)
        self.classSymbolTable = SymbolTable()
        self.methodSymbolTable = SymbolTable()
        self.output_stream = output_stream

    # DONE
    def eat_token(self):
        """ Return the current token and advances the tokenizer"""

        # keep the current token
        if self.tokenizer.get_token() in SPECIAL_SYMBOLS:
            token = SPECIAL_SYMBOLS[self.tokenizer.get_token()]
        else:
            token = self.tokenizer.get_token()

        # advances the tokenizer
        self.tokenizer.advance()

        return token

    def compile_class(self) -> None:
        """ Compile a class frame
        """

        # <class>
        self.output_stream.write("<class>\n")
        self.tokenizer.advance()

        # <keyword> class </keyword>
        self.eat_token()

        # <identifier> className </identifier>
        self.eat_token()

        # <symbol> { </symbol>
        self.eat_token()

        # // classVarDec - recursive
        while self.tokenizer.get_token() in CLASS_VAR:
            self.compile_class_var_dec()

        # // subroutineDec - recursive
        while self.tokenizer.get_token() in SUBROUTINE:
            self.compile_subroutine()

        # <symbol> } </symbol>
        self.eat_token()

        # </class>
        self.output_stream.write("</class>\n")

    def addToSymbolTable(self, table, type, kind, separator):
        """ Compile the sentence:
        varName (, varName)*
        by adding the variables declared to the given symbolTable
        """
        first = True

        # compile varName (, varName)*
        while self.tokenizer.get_token() == separator or first:

            if not first:
                # current token is the separator, dump it
                self.eat_token()

            # type is None iff the case is of a parameter list, where
            # the types can vary from variable to another
            if type is None:
                # current token is the type
                type = self.eat_token()

            # current token is the name
            name = self.eat_token()

            # add the variable to the current symbolTable
            table.define(name, type, kind)

            first = False

    # DONE
    def compile_class_var_dec(self) -> None:
        """ Compile a class variable declaration -
         Add them to the main symbolTable
        """

        # current token is the kind
        kind = self.eat_token()

        # current token is the type
        type = self.eat_token()

        # add the variables to the class symbolTable
        self.addToSymbolTable(self.classSymbolTable, type, CLASS_VAR_TO_SEG[kind], ',')

        # current token is ";", dump it
        self.eat_token()

    def reset_methodSymbolTable(self):
        """
        resets the current method SymbolTable to a new method scope
        """
        self.methodSymbolTable.start_subroutine()
        self.methodSymbolTable.define("this", self.class_type, ARG)

    def compile_subroutine(self) -> None:
        """ Compile a subroutine declaration:
        add the name of the method to the symbolTable, and creat a new local
        symbolTable initialized with "this" variable.
        """

        # current token is the type - (constructor|method|function)
        type = self.eat_token()

        # current token is the return type
        return_type = self.eat_token()

        # current token is the name
        name = self.eat_token()

        # current token is "(", dump it
        self.eat_token()

        # resets the subroutine symbolTable for a new scope
        self.reset_methodSymbolTable()

        # next tokens are the argument of the subroutine - add them
        # to a the new subroutine symbolTable
        self.compile_parameter_list()

        # current token is ")", dump it
        self.eat_token()

        # // subroutineBody - recursive
        self.compile_subroutineBody()

    # DONE
    def compile_parameter_list(self) -> None:
        """Compiles parameter list of a subroutine - add them to the
        right symbolTable
        """

        if self.tokenizer.get_token() != ')':
            self.addToSymbolTable(self.methodSymbolTable, None, ARG, ',')

    # DONE
    def compile_var_dec(self) -> None:
        """Compile local variable declarations"""

        # current token is "var", dump it
        self.eat_token()

        # current token is the type
        type = self.eat_token()

        # add the variables to the method symbolTable
        self.addToSymbolTable(self.methodSymbolTable, type, LCL, ',')

        # current token is ";", dump it
        self.eat_token()

    def compile_statements(self) -> None:
        """Compiles a sequence of statements, not including the enclosing 
        "{}":
        <statements>
        [doStatement|letStatement|whileStatement|returnStatement|ifStatement]*
        </statements>
        """

        # <statements>
        self.output_stream.write("<statements>\n")

        while self.tokenizer.get_token() in STATEMENTS:
            if self.tokenizer.get_token() == 'let':
                self.compile_let()
            elif self.tokenizer.get_token() == 'do':
                self.compile_do()
            elif self.tokenizer.get_token() == 'while':
                self.compile_while()
            elif self.tokenizer.get_token() == 'if':
                self.compile_if()
            elif self.tokenizer.get_token() == 'return':
                self.compile_return()

        # </statements>
        self.output_stream.write("</statements>\n")

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
        self.eat_token()

        # // subroutineCall - recursive
        self.compile_subroutine_call()

        # <symbol> ; </symbol>
        self.eat_token()

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
        self.eat_token()

        # <identifier> varName </identifier>
        self.eat_token()

        if self.tokenizer.get_token() == '[':
            # <symbol> [ </symbol>
            self.eat_token()

            # // expression - recursive
            self.compile_expression()

            # <symbol> ] </symbol>
            self.eat_token()

        # <symbol> = </symbol>
        self.eat_token()

        # // expression - recursive
        self.compile_expression()

        # <symbol> ; </symbol>
        self.eat_token()

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
        self.eat_token()

        # <symbol> ( </symbol>
        self.eat_token()

        # // expression - recursive
        self.compile_expression()

        # <symbol> ) </symbol>
        self.eat_token()

        # <symbol> { </symbol>
        self.eat_token()

        # // statements - recursive
        self.compile_statements()

        # <symbol> } </symbol>
        self.eat_token()

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
        self.eat_token()

        # // expression? - recursive
        if self.tokenizer.get_token() != ';':
            self.compile_expression()

        # <symbol> ; </symbol>
        self.eat_token()

        # </returnStatement>
        self.output_stream.write("</returnStatement>\n")

    def compile_if(self) -> None:
        """ Compile a let statement:

        """

        # <ifStatement>
        self.output_stream.write("<ifStatement>\n")

        # <keyword> if </keyword>
        self.eat_token()

        # <symbol> ( </symbol>
        self.eat_token()

        # // expression - recursive
        self.compile_expression()

        # <symbol> ) </symbol>
        self.eat_token()

        # <symbol> { </symbol>
        self.eat_token()

        # // statements - recursive
        self.compile_statements()

        # <symbol> } </symbol>
        self.eat_token()

        # //else?
        if self.tokenizer.get_token() == 'else':
            # <keyword> else </keyword>
            self.eat_token()

            # <symbol> { </symbol>
            self.eat_token()

            # // statements - recursive
            self.compile_statements()

            # <symbol> } </symbol>
            self.eat_token()

        # </ifStatement>
        self.output_stream.write("</ifStatement>\n")

    def compile_expression(self) -> None:
        """Compiles an expression:
        term [op term]* :
        <expression>
            // term ...
            // optional more op term ...
        </expression>
        """
        # <expression>
        self.output_stream.write("<expression>\n")

        # // term - NOT recursive! Since if there is a recursive grammar,
        # the compile_additional_op_term does it
        self.compile_term()

        # // optional more op term - recursive
        self.compile_optional_terms(OP, self.compile_term)

        #  </expression>
        self.output_stream.write("</expression>\n")

    def compile_term(self) -> None:
        """ Compiles a single statement
        """

        if self.tokenizer.token_type() in CONSTANTS:
            # <(stringConstant|integerConstant|keyword> term </(stringConstant|integerConstant|keyword>
            self.eat_token()

        elif self.tokenizer.get_token() == '(':
            # <symbol> ( </symbol>
            self.eat_token()

            # expression ...
            self.compile_expression()

            # <symbol> ) </symbol>
            self.eat_token()

        elif self.tokenizer.get_token() in UNARY_OP:
            # <symbol> unaryOp </symbol>
            self.eat_token()

            # // term ...
            self.compile_term()

        else:
        # current token is an identifier. print it and advance token:

            # <identifier> name </identifier>
            self.eat_token()

            if self.tokenizer.get_token() == '[':
                # <symbol> [ </symbol>
                self.eat_token()

                # // expression - recursive
                self.compile_expression()

                # <symbol> ] </symbol>
                self.eat_token()

            elif self.tokenizer.get_token() == '.':
                self.compile_subroutine_call(print_identifier=False)

            elif self.tokenizer.get_token() == '(':
                # <symbol> ( </symbol>
                self.eat_token()

                # expressionList ...
                self.compile_expression_list()

                # <symbol> ) </symbol>
                self.eat_token()

        # </term>
        self.output_stream.write("</term>\n")

    def compile_expression_list(self) -> None:
        """Compiles a (possibly empty) comma-separated list of expressions:
        [expression[',' expression]*]? :
        <expressionList>
            // expression ...
            // optional more expressions ...
        </expressionList>
        """

        # <expressionList>
        self.output_stream.write("<expressionList>\n")

        # // expression ...
        if self.tokenizer.get_token() != ')':
            self.compile_expression()

            # // optional more expressions ...
            self.compile_optional_terms([','], self.compile_expression)

        #  </expressionList>
        self.output_stream.write("</expressionList>\n")

    def compile_subroutine_call(self, print_identifier=True) -> None:

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

        if print_identifier:
            # <identifier> mainName </identifier>
            self.eat_token()

        if self.tokenizer.get_token() == '(':
            pass

        else:
            # <symbol> . </symbol>
            self.eat_token()

            # <identifier> subName </identifier>
            self.eat_token()

        # <symbol> '(' </symbol>
        self.eat_token()

        # // expressionList - recursive
        self.compile_expression_list()

        # <symbol> ')' </symbol>
        self.eat_token()

    def compile_subroutineBody(self):
        """ Compile a subroutineBody variables & statements
        """

        # <subroutineBody>
        self.output_stream.write("<subroutineBody>\n")

        # <symbol> { </symbol>
        self.eat_token()

        # // varDec - recursive
        while self.tokenizer.get_token() == 'var':
            self.compile_var_dec()

        # // statements - recursive
        self.compile_statements()

        # <symbol> } </symbol>
        self.eat_token()

        # </subroutineBody>
        self.output_stream.write("</subroutineBody>\n")

    def compile_optional_terms(self, separators, compiler, parameters=False):
        """Compile an additional optional grammar terms, called for one of:
        1) [op term]*
        2) (',' varName)
        3) (',' type varName)
        4) (',' expression)
        etc.
        :param separators: list of symbols separates between terms: (op|',')
        :param compiler: a callable function, one of the follow:
                        self.compile_term >>> for case 1
                        self.write_token >>> for cases 2, 3
                        self.compile_expression >>> for case 4
        :param parameters: True iff type is 3)
        """
        while self.tokenizer.get_token() in separators:

            # current token is the separator, dump it
            _ = self.eat_token()

            if parameters:
                # <(keyword|identifier)> type </(keyword|identifier)>
                self.eat_token()

            # call the compiler method.
            compiler()

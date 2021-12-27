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
        self.label_count = 0

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

    def find_symbol(self, symbol : str) -> list:
        pass

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
        add the name of the method to the symbolTable, and create a new local
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
        # to the new subroutine symbolTable
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
        """

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

    # DONE
    def compile_do(self) -> None:
        """Compiles a do statement"""

        # current token is "do", dump it
        self.eat_token()

        # // subroutineCall - recursive
        self.compile_subroutine_call()

        # # current token is ";", dump it
        self.eat_token()


    def compile_let(self) -> None:
        """Compiles a let statement"""

        # current token is "let", dump it
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

    # DONE
    def compile_while(self) -> None:
        """Compiles a while statement"""

        L1 = "L1.%d" % self.label_count
        L2 = "L2.%d" % self.label_count

        # label L1
        self.writer.write_label(L1)
        # current token is "while", dump it
        self.eat_token()
        # current token is "(", dump it
        self.eat_token()

        # compile expression
        self.compile_expression()
        # current token is ")", dump it
        self.eat_token()
        # current token is "{", dump it
        self.eat_token()

        # neg
        self.writer.write_arithmetic(NEG)

        # if-goto L2
        self.writer.write_if(L2)

        # compile statements
        self.compile_statements()
        # current token is "}", dump it
        self.eat_token()

        # goto L1
        self.writer.write_goto(L1)

        # label L2
        self.writer.write_label(L2)

    # DONE
    def compile_return(self) -> None:
        """Compiles a return statement"""

        # current token is "return", dump it
        self.eat_token()

        # if there is any expression to return
        if self.tokenizer.get_token() != ';':
            # compile expression
            self.compile_expression()

        # return
        self.writer.write_return()
        # current token is ";", dump it
        self.eat_token()

    # DONE
    def compile_if(self) -> None:
        """ Compile an if statement """

        L1 = "L1.%d" % self.label_count
        L2 = "L2.%d" % self.label_count

        # current token is "if", dump it
        self.eat_token()
        # current token is "(", dump it
        self.eat_token()

        # compile expression
        self.compile_expression()
        # current token is ")", dump it
        self.eat_token()
        # current token is "{", dump it
        self.eat_token()

        # neg
        self.writer.write_arithmetic(NEG)

        # if-goto L1
        self.writer.write_if(L1)

        # compile statements1
        self.compile_statements()
        # current token is "}", dump it
        self.eat_token()

        # goto L2
        self.writer.write_goto(L2)

        # label L1
        self.writer.write_label(L1)

        # if there is any else statement
        if self.tokenizer.get_token() == 'else':
            # current token is "else", dump it
            self.eat_token()
            # current token is "{", dump it
            self.eat_token()
            # compile statements2
            self.compile_statements()
            # current token is "}", dump it
            self.eat_token()

        # label L2
        self.writer.write_label(L2)

    def compile_expression_for_call(self, name):
        # current token is "(", dump it
        self.eat_token()

        # compile exp1, exp2, ...
        nArgs = self.compile_expression_list()

        # call exp1 nArgs
        self.writer.write_call(name, nArgs)
        # current token is ")", dump it
        self.eat_token()

    def compile_expression(self) -> None:
        """Compiles an expression"""

        # first term of the expression
        exp1 = self.eat_token()

        if exp1 in UNARY_OP:
            # compile exp1 and OP

        if self.tokenizer.get_token() in OP :
            # compile exp1, exp2 and OP

        # if token is"(", so this is a subroutine call
        if self.tokenizer.get_token() == '(' or '.':
            if self.tokenizer.get_token() == '.':
                # construct the full name: "class.name"
                exp1 += self.eat_token() + self.eat_token()
            # compile the subroutine call
            self.compile_expression_for_call(exp1)

        # // optional more op term - recursive
        self.compile_optional_terms(OP, self.compile_term)

    def compile_term(self, exp) -> str:
        """ Compiles a single term"""

        if self.tokenizer.token_type() in CONSTANTS:
            # <(stringConstant|integerConstant|keyword> term </(stringConstant|integerConstant|keyword>
            exp += self.eat_token()

        elif self.tokenizer.get_token() == '(':
            # <symbol> ( </symbol>
            exp += self.eat_token()

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

    def compile_expression_list(self) -> int:
        """Compiles an expression list. This if called only from a subroutine
        call compiler, where the expressions are not needed but their count
        does
        """

        counter = 0

        # if there is any expression
        if self.tokenizer.get_token() != ')':

            # TODO: change this function
            self.compile_expression()
            counter+=1

            # optional more expressions ...
            while self.tokenizer.get_token() == ',':
                self.compile_expression()
                counter+=1

        return counter

    # DONE
    def compile_subroutine_call(self) -> None:

        """Compile a subroutineCall:
        call (class.)*foo nArgs
         """

        # current token is a name - might be a class name
        name = self.eat_token()

        if self.tokenizer.get_token() == '(':
            pass

        else:
            # current token is ".", add it to name
            name += self.eat_token()

            # current token is the name of the subroutine
            name += self.eat_token()

        # current token is "(", dump it
        self.eat_token()

        # count number of arguments for the call
        nArgs = self.compile_expression_list()

        # current token is ")", dump it
        self.eat_token()

        # call foo nArgs
        self.writer.write_call(name, nArgs)

    def compile_subroutineBody(self):
        """ Compile a subroutineBody variables & statements
        """

        # current token is "{", dump it
        self.eat_token()

        # // varDec - recursive
        while self.tokenizer.get_token() == 'var':
            self.compile_var_dec()

        # // statements - recursive
        self.compile_statements()

        # current token is "}", dump it
        self.eat_token()



    ############################## OLD ####################
    # def compile_optional_terms(self, separators, compiler, parameters=False):
    #     """Compile an additional optional grammar terms, called for one of:
    #     1) [op term]*
    #     2) (',' varName)
    #     3) (',' type varName)
    #     4) (',' expression)
    #     etc.
    #     :param separators: list of symbols separates between terms: (op|',')
    #     :param compiler: a callable function, one of the follow:
    #                     self.compile_term >>> for case 1
    #                     self.write_token >>> for cases 2, 3
    #                     self.compile_expression >>> for case 4
    #     :param parameters: True iff type is 3)
    #     """
    #     while self.tokenizer.get_token() in separators:
    #
    #         # current token is the separator, dump it
    #         _ = self.eat_token()
    #
    #         if parameters:
    #             # <(keyword|identifier)> type </(keyword|identifier)>
    #             self.eat_token()
    #
    #         # call the compiler method.
    #         compiler()

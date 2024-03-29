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
        self.field_count = 0
        self.type = ""

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

    # DONE
    def compile_class(self) -> None:
        """ Compile a class frame
        """

        # starter
        self.tokenizer.advance()

        # current token is "class", dump it
        self.eat_token()

        # current token is the type of this class object, keep it as a field
        self.type = self.eat_token()

        # current token is "{", dump it
        self.eat_token()

        # // classVarDec - recursive
        while self.tokenizer.get_token() in CLASS_VAR:
            self.compile_class_var_dec()

        # // subroutineDec - recursive
        while self.tokenizer.get_token() in SUBROUTINE:
            self.compile_subroutine()

        # current token is "}", dump it
        self.eat_token()

    # DONE
    def find_symbol(self, symbol : str, type=False):
        """
        Find a given symbol representation: it's segment and it's index
        """
        if self.methodSymbolTable.kind_of(symbol):
            if type:
                return self.methodSymbolTable.type_of(symbol)
            return self.methodSymbolTable.kind_of(symbol),\
                   self.methodSymbolTable.index_of(symbol)
        if type:
            return self.classSymbolTable.type_of(symbol)
        return self.classSymbolTable.kind_of(symbol),\
               self.classSymbolTable.index_of(symbol)

    # DONE
    def addToSymbolTable(self, table, type, kind, separator):
        """ Compile the sentence:
        varName (, varName)*
        by adding the variables declared to the given symbolTable
        """
        first = True
        getType = True if type is None else False

        # compile varName (, varName)*
        while self.tokenizer.get_token() == separator or first:

            if not first:
                # current token is the separator, dump it
                self.eat_token()

            # type is None iff the case is of a parameter list, where
            # the types can vary from variable to another
            if getType:
                # current token is the type
                type = self.eat_token()

            # current token is the name
            name = self.eat_token()

            # add the variable to the current symbolTable
            table.define(name, type, kind)

            # id var is field, update field count
            if kind == FIELD:
                self.field_count += 1

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

    # DONE
    def reset_methodSymbolTable(self):
        """
        resets the current method SymbolTable to a new method scope
        """
        self.methodSymbolTable.start_subroutine()

    # DONE
    def allocate(self):
        """
        Allocate memory for the class object
        """
        self.writer.write_push(CONST, self.field_count)
        self.writer.write_call("Memory.alloc", 1)
        self.writer.write_pop(POINTER, 0)

    # DONE
    def compile_subroutine(self) -> None:
        """ Compile a subroutine declaration:
        add the name of the method to the symbolTable, and create a new local
        symbolTable initialized with "this" variable.
        """

        # resets the subroutine symbolTable for a new scope
        self.reset_methodSymbolTable()

        # current token is the type - (constructor|method|function)
        type = self.eat_token()

        if type == 'method':
            self.methodSymbolTable.define('this', self.type, ARG)

        # current token is the return type
        return_type = self.eat_token()

        # current token is the name
        name = self.type + "." + self.eat_token()

        # current token is "(", dump it
        self.eat_token()

        # next tokens are the argument of the subroutine - add them
        # to the new subroutine symbolTable
        self.compile_parameter_list()

        # current token is ")", dump it
        self.eat_token()

        # // subroutineBody - recursive
        self.compile_subroutineBody(name, type)

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

    # DONE
    def compile_statements(self, subroutine_type=None) -> None:
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
                if subroutine_type == 'constructor':
                    self.writer.write_push(POINTER, 0)
                    self.writer.write_return()
                    self.eat_token()     # 'return'
                    self.eat_token()     # 'this'
                    self.eat_token()     # ';'
                else:
                    self.compile_return()

    # DONE
    def compile_do(self) -> None:
        """Compiles a do statement"""

        # current token is "do", dump it
        self.eat_token()

        # subroutineCall
        self.compile_subroutine_call()

        # pop temp 0
        self.writer.write_pop(TEMP, 0)

        # current token is ";", dump it
        self.eat_token()

    # DONE
    def compile_let(self) -> None:
        """Compiles a let statement"""

        # current token is "let", dump it
        self.eat_token()

        # current token is the name
        varName = self.eat_token()

        isArray = False
        if self.tokenizer.get_token() == '[':
            isArray = True
            # current token is'[', dump it
            self.eat_token()

            # push arrName
            self.writer.write_push(*self.find_symbol(varName))

            # this expression represents an index of an array.
            # push index
            self.compile_expression()

            # add
            self.writer.write_arithmetic('+')

            # current token is']', dump it
            self.eat_token()
        # current token is '=', dump it
        self.eat_token()

        # compile expression - push right hand side
        self.compile_expression()

        if isArray:
            # pop temp 0
            self.writer.write_pop(TEMP, 0)

            # pop pointer 1
            self.writer.write_pop(POINTER, 1)

            # push temp 0
            self.writer.write_push(TEMP, 0)

            # pop that 0
            self.writer.write_pop(THAT, 0)

        else:
            # pop varName
            self.writer.write_pop(*self.find_symbol(varName))

        # dump ';'
        self.eat_token()

    # DONE
    def compile_while(self) -> None:
        """Compiles a while statement"""

        L1, L2 = self.get_labels()

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
        self.writer.write_arithmetic('~')

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

    def get_labels(self):
        """Return unique name for labels"""
        L1 = "L1.%d" % self.label_count
        L2 = "L2.%d" % self.label_count
        self.label_count += 1

        return L1, L2

    # DONE
    def compile_if(self) -> None:
        """ Compile an if statement """

        L1, L2 = self.get_labels()

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
        self.writer.write_arithmetic('~')

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

    # DONE
    def compile_expression_for_call(self, name):
        # current token is "(", dump it
        self.eat_token()

        # compile exp1, exp2, ...
        nArgs = self.compile_expression_list()

        # call exp1 nArgs
        if "." not in name:
            name = self.type + "." + name
            # push pointer 0
            self.writer.write_pop(POINTER, 0)
            nArgs += 1
        self.writer.write_call(name, nArgs)
        # current token is ")", dump it
        self.eat_token()

    def compile_expression(self) -> None:
        """Compiles an expression"""

        token = self.tokenizer.get_token()

        if self.tokenizer.token_type() == KEYWORD:
            token = self.eat_token()
            if token == "true":
                self.writer.write_push(CONST, 1)
                self.writer.write_arithmetic('--')
            elif token in ["false", "null"]:
                self.writer.write_push(CONST, 0)
            elif token == "this":
                self.writer.write_push(*self.find_symbol(token))

        if self.tokenizer.get_token() == '(':
            self.eat_token()
            self.compile_expression()
            self.eat_token()
            if self.tokenizer.get_token() in OP:
                op = self.eat_token()
                self.compile_expression()
                self.writer.write_arithmetic(op)

        # first term of the expression is constant integer.
        if self.tokenizer.token_type() == INTEGER_CONSTANT:
            self.writer.write_push("constant", token)
            self.eat_token()

            if self.tokenizer.get_token() in OP:
                op = self.eat_token()
                self.compile_expression()
                self.writer.write_arithmetic(op)

        if self.tokenizer.token_type() == STRING_CONSTANT:
            self.writer.write_string(token)
            self.eat_token()

        # first term of the expression is identifier.
        elif self.tokenizer.token_type() == TOKEN_TYPES_REGEX[IDENTIFIER]:
            cur = token
            self.eat_token()
            this_obj = True
            obj = self.type
            if self.tokenizer.get_token() == '.':
                this_obj = False
                obj = cur
                self.eat_token()
                name = self.eat_token()
            else:
                name = cur
            if self.tokenizer.get_token() == '(':
                self.eat_token()

                nArgs = 0

                # push obj
                if this_obj:
                    self.writer.write_push(POINTER, 0)
                    nArgs += 1
                else:
                    if self.find_symbol(obj, type=True) is not None:
                        self.writer.write_push(*self.find_symbol(obj))
                        obj = self.find_symbol(obj, type=True)
                        nArgs += 1

                # count number of arguments for the call
                nArgs += self.compile_expression_list()

                # current token is ")"
                self.eat_token()

                # call (obj.)?foo nArgs
                self.writer.write_call(obj + "." + name, nArgs)


            elif self.tokenizer.get_token() == '[':
                self.eat_token()
                self.writer.write_push(*self.find_symbol(cur))
                self.compile_expression()
                self.eat_token()
                self.writer.write_arithmetic('+')
                self.writer.write_pop("pointer", 1)
                self.writer.write_push("that", 0)

            else:
                self.writer.write_push(*self.find_symbol(cur))

            if self.tokenizer.get_token() in OP:
                op = self.eat_token()
                self.compile_expression()
                self.writer.write_arithmetic(op)

        elif self.tokenizer.get_token() in UNARY_OP:
            op = self.eat_token()
            self.compile_expression()
            self.writer.write_arithmetic(op + op if op == '-' else op)

    # DONE
    def compile_expression_list(self) -> int:
        """Compiles an expression list. This if called only from a subroutine
        call compiler, where the expressions are not needed but their count
        does
        """

        counter = 0

        # if there is any expression
        if self.tokenizer.get_token() != ')':

            self.compile_expression()
            counter+=1

            # optional more expressions ...
            while self.tokenizer.get_token() == ',':
                self.eat_token()
                self.compile_expression()
                counter+=1

        return counter

    # DONE
    def compile_subroutine_call(self) -> None:

        """Compile a subroutineCall:
        call (class.)?foo nArgs
         """

        # default: the caller is this object
        this_obj = True
        obj = self.type

        # current token is name - maybe an object name
        name = self.eat_token()

        # if current token is "." so the name is actually an object
        # and the next token is name of the subroutine
        if self.tokenizer.get_token() == '.':
            this_obj = False
            obj = name

            # current token is "."
            self.eat_token()

            # current token is the name of the subroutine
            name = self.eat_token()

        nArgs = 0

        # push obj
        if this_obj:
            self.writer.write_push(POINTER, 0)
            nArgs += 1
        else:
            if self.find_symbol(obj, type=True) is not None:
                self.writer.write_push(*self.find_symbol(obj))
                obj = self.find_symbol(obj, type=True)
                nArgs += 1

        # current token is "("
        self.eat_token()

        # count number of arguments for the call
        nArgs += self.compile_expression_list()

        # current token is ")"
        self.eat_token()

        # call (obj.)?foo nArgs
        self.writer.write_call(obj + "." + name, nArgs)

    # DONE
    def compile_subroutineBody(self, name, subroutine_type):
        """ Compile a subroutineBody variables & statements"""

        # current token is "{", dump it
        self.eat_token()

        # // varDec - recursive
        while self.tokenizer.get_token() == 'var':
            self.compile_var_dec()
        local_var_count = self.methodSymbolTable.var_count(VAR)
        self.writer.write_function(name, local_var_count)

        if subroutine_type == 'constructor':
            self.allocate()

        elif subroutine_type == 'method':
            # push argument 0
            self.writer.write_push(ARG, 0)

            # pop pointer 0
            self.writer.write_pop(POINTER, 0)

        # // statements - recursive
        self.compile_statements(subroutine_type)

        # current token is "}", dump it
        self.eat_token()
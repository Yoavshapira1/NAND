"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
from JackTokenizer import JackTokenizer

TERMINALS = ["keyword", "identifier", "integerConstant", "stringConstant", "symbol"]
CONSTANTS = ["integerConstant", "stringConstant", "keyword"]
NON_TERMINALS = ["class", "classVarDec","subroutineDec", "parameterList",
                 "subroutineBody", "varDec", "statements", "LetStatement",
                 "ifStatement", "whileStatement", "doStatement", "returnStatement",
                 "expression", "term", "expressionList"]

STATEMENTS = ['let', 'while', 'if', 'do', 'return']
OP = ['+', '-', '*', '/', '&', '|', '>', '<', '=']
UNARY_OP = ['-', '~']

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

    def write_token(self):
        """ Output for types: keyword, symbols, constant, identifier"""

        # <token_Type>
        opening = '<{}>'.format(self.tokenizer.cur_token_type)

        # <token>
        val = ' ' + self.tokenizer.cur_token + ' '

        # </token_Type>
        closing = '</{}>\n'.format(self.tokenizer.cur_token_type)

        self.output_stream.write(opening + val + closing)

        # advances the tokenizer
        self.tokenizer.advance()

    def compile_class(self) -> None:
        """Compiles a complete class:
        'class' className '{' [classVarDec]* [subroutineDec]* '}' :
        <class>
            <keyword> class </keyword>
            <identifier> className </identifier>
            <symbol> { </symbol>
            // classVarDec ...
            // subroutineDec ...
            <symbol> } </symbol>
        </class>
        """

        # <class>
        self.output_stream.write("<class>\n")

        # <keyword> class </keyword>
        self.write_token()

        # <identifier> className </identifier>
        self.write_token()

        # <symbol> { </symbol>
        self.write_token()

        # // classVarDec - recursive
        self.compile_class_var_dec()

        # // subroutineDec - recursive
        self.compile_subroutine()

        # <symbol> } </symbol>
        self.write_token()

        # </class>
        self.output_stream.write("</class>\n")

    def compile_class_var_dec(self) -> None:
        """Compiles a static declaration or a field declaration:
        ('static'|'field') type varName [',' varName]* ';' :
        <classVarDec>
            <keyword> ('static'|'field') </keyword>
            <(keyword|identifier)> type </(keyword|identifier)>
            <identifier> varName </identifier>
            // optional varNames ...
            <symbol> ; </symbol>
        </classVarDec>
        """

        # <classVarDec>
        self.output_stream.write("<classVarDec>\n")

        # <keyword> (static|field) </keyword>
        self.write_token()

        # <(keyword|identifier)> type </(keyword|identifier)>
        self.write_token()

        # <identifier> varName </identifier>
        self.write_token()

        # // optional varName
        self.compile_optional_terms([','], self.write_token())

        # <symbol> ; </symbol>
        self.write_token()

        # </classVarDec>
        self.output_stream.write("</classVarDec\n>")

    def compile_subroutine(self) -> None:
        """Compiles a complete method, function, or constructor:
        <subroutineDec>
            <keyword> ('constructor'|'function'|'method') </keyword>
            <(keyword|identifier)> ('void'\type) </(keyword|identifier)>
            <identifier> subroutineName </identifier>
            <symbol> ( </symbol>
            // parameterList ...
            <symbol> ) </symbol>
            // subroutineBody ...
        </subroutineDec>
        """

        # <subroutineDec>
        self.output_stream.write("<subroutineDec>\n")

        # <keyword> ('constructor'|'function'|'method') </keyword>
        self.write_token()

        # <(keyword|identifier)> ('void'|type) </(keyword|identifier)>
        self.write_token()

        # <identifier> subroutineName </identifier>
        self.write_token()

        # <symbol> ( </symbol>
        self.write_token()

        # // parameterList - recursive
        self.compile_parameter_list()

        # <symbol> ) </symbol>
        self.write_token()

        # // subroutineBody - recursive
        self.compile_subroutineBody()

        # </subroutineDec>
        self.output_stream.write("</subroutineDec>\n")

    def compile_parameter_list(self) -> None:
        """Compiles a (possibly empty) parameter list, not including the 
        enclosing "()":
        [(type varName) [',' type varName]*]? :
        <parameterList>
          [<(keyword|identifier)> type </(keyword|identifier)>
          <identifier> varName </identifier>]?
          // optional more parameters ...
        </parameterList>
        """

        # <parameterList>
        self.output_stream.write("<parameterList\n>")

        if self.tokenizer.cur_token != ')':

            # <(keyword|identifier)> type </(keyword|identifier)>
            self.write_token()

            # <identifier> varName </identifier>
            self.write_token()

            # // optional more parameters
            self.compile_optional_terms([','], self.write_token(), parameters=True)

        # </parameterList>
        self.output_stream.write("</parameterList\n>")

    def compile_var_dec(self) -> None:
        """Compiles a var declaration:
        <varDec>
            <keyword> var </keyword>
            <(keyword|identifier)> ('void'\type) </(keyword|identifier)>
            <identifier> varName </identifier>
            // optional varNames ...
            <symbol> ; </symbol>
        </varDec>
        """

        # <varDec>
        self.output_stream.write("<varDec>\n")

        # <keyword> var </keyword>
        self.write_token()

        # <(keyword|identifier)> ('int'|'boolean'|'char'|type) </(keyword|identifier)>
        self.write_token()

        # <identifier> varName </identifier>
        self.write_token()

        # // optional varNames ...
        self.compile_optional_terms([','], self.write_token())

        # <symbol> ; </symbol>
        self.write_token()

        # </varDec>
        self.output_stream.write("</varDec>\n")

    def compile_statements(self) -> None:
        """Compiles a sequence of statements, not including the enclosing 
        "{}":
        <statements>
        [doStatement|letStatement|whileStatement|returnStatement|ifStatement]*
        </statements>
        """

        # <statements>
        self.output_stream.write("<statements>\n")

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
        self.write_token()

        # // subroutineCall - recursive
        self.compile_subroutine_call()

        # <symbol> ; </symbol>
        self.write_token()

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
        self.write_token()

        # <identifier> varName </identifier>
        self.write_token()

        if self.tokenizer.cur_token == '[':
            # <symbol> [ </symbol>
            self.write_token()

            # // expression - recursive
            self.compile_expression()

            # <symbol> ] </symbol>
            self.write_token()

        # <symbol> = </symbol>
        self.write_token()

        # // expression - recursive
        self.compile_expression()

        # <symbol> ; </symbol>
        self.write_token()

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
        self.output_stream.write("<while>\n")

        # <symbol> ( </symbol>
        self.write_token()

        # // expression - recursive
        self.compile_expression()

        # <symbol> ) </symbol>
        self.write_token()

        # <symbol> { </symbol>
        self.write_token()

        # // statements - recursive
        self.compile_statements()

        # <symbol> } </symbol>
        self.write_token()

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
        self.write_token()

        # // expression? - recursive
        if self.tokenizer.cur_token() != ';':
            self.compile_expression()

        # <symbol> ; </symbol>
        self.write_token()

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
        self.write_token()

        # <symbol> ( </symbol>
        self.write_token()

        # // expression - recursive
        self.compile_expression()

        # <symbol> ) </symbol>
        self.write_token()

        # <symbol> { </symbol>
        self.write_token()

        # // statements - recursive
        self.compile_statements()

        # <symbol> } </symbol>
        self.write_token()

        # //else?
        if self.tokenizer.cur_token == 'else':
            # <keyword> else </keyword>
            self.write_token()

            # <symbol> { </symbol>
            self.write_token()

            # // statements - recursive
            self.compile_statements()

            # <symbol> } </symbol>
            self.write_token()

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
        self.output_stream.write("<expression\n>")

        # // term - NOT recursive! Since if there is a recursive grammar,
        # the compile_additional_op_term does it
        self.compile_term()

        # // optional more op term - recursive
        self.compile_optional_terms(OP, self.compile_term())

        #  </expression>
        self.output_stream.write("</expression\n>")

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

        # <term>
        self.output_stream.write("<term>\n")

        if self.tokenizer.cur_token_type in CONSTANTS:
            # <(stringConstant|integerConstant|keyword> term </(stringConstant|integerConstant|keyword>
            self.write_token()

        elif self.tokenizer.cur_token == '(':
            # <symbol> ( </symbol>
            self.write_token()

            # expression ...
            self.compile_expression()

            # <symbol> ) </symbol>
            self.write_token()

        elif self.tokenizer.cur_token in UNARY_OP:
            # <symbol> unaryOp </symbol>
            self.write_token()

            # // term ...
            self.compile_term()

        else:
        # current token is an identifier. print it and advance token:

            # <identifier> name </identifier>
            self.write_token()

            if self.tokenizer.cur_token == '[':
                # <symbol> [ </symbol>
                self.write_token()

                # // expression - recursive
                self.compile_expression()

                # <symbol> ] </symbol>
                self.write_token()

            elif self.tokenizer.cur_token in ['(', '.']:
                # <symbol> (','|'.') </symbol>
                self.write_token()

                # // subroutineCall - recursive
                self.compile_subroutine_call(print_identifier=(self.tokenizer.cur_token=='.'))

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
        if self.tokenizer.cur_token != ')':
            self.compile_expression()

            # // optional more expressions ...
            self.compile_optional_terms([')'], self.compile_expression())

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
            self.write_token()

        if self.tokenizer.cur_token == '(':
            pass

        else:
            # <symbol> . </symbol>
            self.write_token()

            # <identifier> subName </identifier>
            self.write_token()

        # <symbol> '(' </symbol>
        self.write_token()

        # // expressionList - recursive
        self.compile_expression_list()

        # <symbol> ')' </symbol>
        self.write_token()

    def compile_subroutineBody(self):
        """ Compile a subroutineBody code:
        '{' [varDec]* statements '}' :
        <subroutineBody>
            <symbol> { </symbol>
            // varDec ...
            // statements ...
            <symbol> } </symbol>
        </subroutineBody>
        """

        # <subroutineBody>
        self.output_stream.write("<subroutineBody>\n")

        # <symbol> { </symbol>
        self.write_token()

        # // varDec - recursive
        self.compile_var_dec()

        # // statements - recursive
        self.compile_statements()

        # <symbol> } </symbol>
        self.write_token()

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
        while self.tokenizer.cur_token in separators:

            # <symbol> (','|op) </symbol>
            self.write_token()

            if parameters:
                # <(keyword|identifier)> type </(keyword|identifier)>
                self.write_token()

            # call the compiler method.
            compiler()


    ########## OLD FUNCTIONS - compile_optional_terms replaces them ########

    # def compile_additional_varName(self, parameters=False):
    #     """Compile optional varDec:
    #     ',' varName :
    #     # <symbol> , </symbol>
    #     # <identifier> varName </identifier>
    #     """
    # while self.tokenizer.cur_token == ',':
    #
    #     # <symbol> , </symbol>
    #     self.write_token()
    #
    #     if parameters:
    #         # <(keyword|identifier)> type </(keyword|identifier)>
    #         self.write_token()
    #
    #     # <identifier> varName </identifier>
    #     self.write_token()

    # def compile_additional_op_term(self):
    #     """Compile additional [op term] grammar that follows a term:
    #     [op term]* :
    #     <symbol> op </symbol>
    #     // term
    #     """
    #
    #     while self.tokenizer.cur_token_type in OP:
    #         # <symbol> op </symbol>
    #         self.write_token()
    #
    #         # // term ...
    #         self.compile_term()
    #
    # def compile_additional_expressions(self):
    #     """Compile additional [',' expression] grammar that follows a expresion
    #     <symbol> , </symbol>
    #     // expression
    #     """
    #
    #     while self.tokenizer.cur_token_type  == ',':
    #         # <symbol> , </symbol>
    #         self.write_token()
    #
    #         # // expression ...
    #         self.compile_expression()


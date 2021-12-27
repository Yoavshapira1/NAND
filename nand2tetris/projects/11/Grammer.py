import re


KEYWORDS = "(class|method|function|constructor|int|" \
           "boolean|char|void|var|static|field|let|do|" \
           "if|else|while|return|true|false|null|this)"

SYMBOLS = "(\{|\}|\(|\)|\[|\]|\.|,|;|\+|\-|\*|\/|&|\||<|>|=|~|\^|#)"

INTEGER = "[0-9]+"

STRING = "STRING"

IDENTIFIER = "[a-zA-Z_][\w]*"

KEYWORD = "keyword"

SYMBOL = "symbol"

INTEGER_CONSTANT = "integerConstant"

STRING_CONSTANT = "stringConstant"

TOKEN_TYPES_REGEX = {KEYWORDS: KEYWORD,
                     SYMBOLS: SYMBOL,
                     INTEGER: INTEGER_CONSTANT,
                     STRING: STRING_CONSTANT,
                     IDENTIFIER: "identifier"}

ALL_TOKEN_TYPES_REGEX = "(" + IDENTIFIER + "|" + SYMBOLS + "|" + INTEGER + "|" + STRING + "|" + KEYWORDS + ")?"

SPECIAL_SYMBOLS = {"&" : "&amp;", "<" : "&lt;", ">" : "&gt;"}
STATEMENTS = ['let', 'while', 'if', 'do', 'return']
OP = ['+', '-', '*', '/', '&', '|', '>', '<', '=']
UNARY_OP = ['-', '~', '#', '^']
CONSTANTS = [STRING_CONSTANT, INTEGER_CONSTANT, KEYWORD]
SUBROUTINE = ["method", "function", "constructor"]
CLASS_VAR = ["static", "field"]

LCL = "local"
THIS = "this"
THAT = "that"
CONST = "constant"
POINTER = "pointer"
TEMP = "temp"
STATIC = "static"
FIELD = "this"
ARG = "argument"
VAR = "local"

ADD = "add"
SUB = "sub"
EQ = "eq"
GT = "gt"
LT = "lt"
AND = "and"
OR = "or"
NEG = "neg"

# USEFUL DICTIONARIES

CLASS_VAR_TO_SEG = {"static": STATIC, "field": FIELD}
OPERATOR_TO_VM = {"+": ADD, "-": SUB, "&": AND, "|": OR, ">": GT,
                  "<": LT, "=": EQ, "~": NEG}
import re


KEYWORDS = "(class|method|function|constructor|int|" \
           "boolean|char|void|var|static|field|let|do|" \
           "if|else|while|return|true|false|null|this)"

SYMBOLS = "(\{|\}|\(|\)|\[|\]|\.|,|;|\+|\-|\*|\/|&|\||<|>|=|~)"

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


### dont know if needed yet so didnt check all below

# WHITESPACE = "\\s+"
#
# TERM = INTEGER_CONSTANT + "|" + STRING_CONSTANT + "|" + KEYWORDS + "|"
#
# CLASS_NAME = IDENTIFIER
#
# SUBROUTINE_NAME = IDENTIFIER
#
# VAR_NAME = IDENTIFIER
#
# OP = "(\\+|\\-|\\*|\\/|\\&|\\||\\<|\\>|\\=)"
#
# EXPRESSION = TERM + "(" + OP + TERM + ")*"
#
# ARRAY = VAR_NAME + "[" + EXPRESSION + "]"

STATEMENTS = ['let', 'while', 'if', 'do', 'return']
OP = ['+', '-', '*', '/', '&', '|', '>', '<', '=']
UNARY_OP = ['-', '~']
CONSTANTS = [STRING_CONSTANT, INTEGER_CONSTANT, KEYWORD]


##PROBLEMS:
# STRING - except new line
# term + 5 - can be let + 5?

if __name__ == '__main__':
    txt = ""
    x = re.sub(r'\([^)]*\)', '', txt)

    if x:
        print("YES! We have a match!")
        print(x)
    else:
        print("No match")
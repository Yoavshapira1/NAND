import re

KEYWORDS = "(CLASS|METHOD|FUNCTION|CONSTRUCTOR|INT|" \
           "BOOLEAN|CHAR|VOID|VAR|STATIC|FIELD|LET|DO|" \
           "IF|ELSE|WHILE|RETURN|TRUE|FALSE|NULL|THIS)"

SYMBOLS = "(\\{|\\}\\\|\\(|\\)|\\[|\\]|\\.|\\,|\\;|\\+|\\-|\\*|\\/|\\&|\\||\\<|\\>|\\=|\\~)"

WHITESPACE = "\\s+"

INTEGER = "[0-9]+"

STRING = "\d"

TERM = INTEGER + "|" + STRING + "|" + KEYWORDS + "|"

IDENTIFIER = "[a-zA-Z_][\w]*"

CLASS_NAME = IDENTIFIER

SUBROUTINE_NAME = IDENTIFIER

VAR_NAME = IDENTIFIER

LET_STATEMENT = "let"

IF_STATEMENT = "if"

WHILE_STATEMENT = "while"

DO_STATEMENT = "do"

RETURN_STATEMENT = "return"

STATEMENT = LET_STATEMENT + "|" + IF_STATEMENT + "|" + WHILE_STATEMENT + "|" + DO_STATEMENT + "|" + RETURN_STATEMENT

OP = "(\\+|\\-|\\*|\\/|\\&|\\||\\<|\\>|\\=)"

EXPRESSION = TERM + "(" + OP + TERM + ")*"

ARRAY = VAR_NAME + "[" + EXPRESSION + "]"

##PROBLEMS:
# STRING - except new line
# term + 5 - can be let + 5?

if __name__ == '__main__':
    txt = "x+"
    x = re.match(EXPRESSION, txt)

    if x:
        print("YES! We have a match!")
    else:
        print("No match")
import parsy as P


whitespace = P.regex(r'\s*', P.re.MULTILINE)

lexeme = lambda p: p << whitespace

keyword = lambda str: lexeme(P.string(str))

number = lexeme(P.regex(r'(0|[1-9][0-9]*)').map(int))

identifier = lexeme(P.regex(r'[_a-zA-Z][_a-zA-Z0-9]*'))

value = number | identifier

@P.generate
def expression():
    fst = yield value
    rest = yield P.seq(P.char_from("+-*/"), value).many()


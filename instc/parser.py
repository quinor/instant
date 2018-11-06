import parsy as P
from . import ast


whitespace = P.regex(r'\s*', P.re.MULTILINE)

lexeme = lambda p: p << whitespace

reserved = lambda str: lexeme(P.string(str))

parens = lambda p: reserved("(") >> p << reserved(")")

number = lexeme(P.regex(r'(0|[1-9][0-9]*)')).map(int).map(ast.Constant)

identifier = lexeme(P.regex(r"[_a-zA-Z][_'a-zA-Z0-9]*"))

variable = identifier.map(ast.Variable)

operator = lexeme(P.char_from("+-*/")).map(
    lambda x: {"+": ast.Add, "-": ast.Sub, "*": ast.Mul, "/": ast.Div}[x])

value = number | variable


@P.generate
def single_expression():
    return (yield number | variable | parens(expression))


@P.generate
def expression():
    fst = yield single_expression
    rest = yield P.seq(operator, single_expression).map(tuple).many()

    val_stack = [fst]
    op_stack = []

    def apply_op():
        h2 = val_stack.pop()
        h1 = val_stack.pop()
        o = op_stack.pop()
        val_stack.append(ast.Application(h1, h2, o))

    for op, val in rest:
        while len(op_stack) != 0 and (
            op_stack[-1].precedence > op.precedence or
            (op_stack[-1].precedence == op.precedence and op_stack[-1].associativity == "left")
        ):
            apply_op()
        op_stack.append(op)
        val_stack.append(val)

    while len(op_stack) != 0:
        apply_op()
    assert len(val_stack) == 1 and len(op_stack) == 0

    return val_stack[-1]


@P.generate
def assignment():
    name = yield identifier
    yield reserved("=")
    expr = yield expression
    return ast.Assignment(name, expr)

topexpr = expression.map(ast.Result)

tld = whitespace >> ((assignment | topexpr) << reserved(";").optional()).many()

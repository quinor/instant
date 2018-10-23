from . import ast
from . import parser
from . import analysis


def interpret(program):
    decls = parser.tld.parse(program)
    analysis.analize(decls)

    variables = {}

    def compute(expr):
        if isinstance(expr, ast.Application):
            fn = {
                "+": lambda x, y: x+y,
                "-": lambda x, y: x-y,
                "*": lambda x, y: x*y,
                "/": lambda x, y: x//y,
            }[expr.function.symbol]
            return fn(compute(expr.left), compute(expr.right))
        elif isinstance(expr, ast.Variable):
            return variables[expr.name]
        elif isinstance(expr, ast.Constant):
            return expr.value
        else:
            raise Exception("no such node: {}".format(expr))
    for decl in decls:
        val = compute(decl.expression)
        if isinstance(decl, ast.Assignment):
            variables[decl.variable] = val
        elif isinstance(decl, ast.Result):
            print(val)
        else:
            raise Exception("no such TLD: {}".format(expr))

from . import ast

def analize(decls):
    varset = set()

    def vars_exist(expr):
        if isinstance(expr, ast.Variable):
            name = expr.name
            if name not in varset:
                raise Exception("there is no variable {}".format(name))

    for line in decls:
        ast.traverse(line.expression, vars_exist)
        if isinstance(line, ast.Assignment):
            varset.add(line.variable)

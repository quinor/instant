from . import ast
from . import analysis


def interpret(program):
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
    for decl in program:
        val = compute(decl.expression)
        if isinstance(decl, ast.Assignment):
            variables[decl.variable] = val
        elif isinstance(decl, ast.Result):
            print(val)
        else:
            raise Exception("no such TLD: {}".format(expr))


def compile_llvm(program):
    reg_c = 0
    variables = {}
    result_program = []

    result_program.append("declare void @printInt(i32)")
    result_program.append("define i32 @main() {")

    def compute(expr):
        if isinstance(expr, ast.Application):
            nonlocal reg_c
            fn = {
                "+": "add",
                "-": "sub",
                "*": "mul",
                "/": "sdiv",
            }[expr.function.symbol]
            p1 = compute(expr.left)
            p2 = compute(expr.right)
            newid = "%reg{}".format(reg_c)
            reg_c+=1
            result_program.append("{} = {} i32 {}, {}".format(newid, fn, p1, p2))
            return newid
        elif isinstance(expr, ast.Variable):
            return variables[expr.name]
        elif isinstance(expr, ast.Constant):
            return expr.value
        else:
            raise Exception("no such node: {}".format(expr))

    for decl in program:
        val = compute(decl.expression)
        if isinstance(decl, ast.Assignment):
            variables[decl.variable] = val
        elif isinstance(decl, ast.Result):
            result_program.append("call void @printInt(i32 {})".format(val))
        else:
            raise Exception("no such TLD: {}".format(expr))

    result_program.append("ret i32 0")
    result_program.append("}")
    return result_program

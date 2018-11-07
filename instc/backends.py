from . import ast
from . import analysis
from . import resources


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


def llvm_backend(program):
    reg_c = 0
    variables = {}
    result_program = []

    for l in resources.LLVM_RUNTIME.split("\n"):
        result_program.append(l)

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
            result_program.append("    {} = {} i32 {}, {}".format(newid, fn, p1, p2))
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
            result_program.append("    call void @printInt(i32 {})".format(val))
        else:
            raise Exception("no such TLD: {}".format(expr))

    result_program.append("    ret i32 0")
    result_program.append("}")
    return "".join(e+"\n" for e in result_program)

def jvm_backend(program, classname):
    var_num = 1
    var_counter = 1
    variables = {}
    result_program = []

    for l in resources.JVM_RUNTIME.format(classname).split("\n"):
        result_program.append(l)

    def optimize(tree):
        if isinstance(tree, ast.Application):
            left, lh = optimize(tree.left)
            right, rh = optimize(tree.right)
            if lh < rh and tree.function.commutativeness:
                right, left = left, right
                rh, lh = lh, rh
            return ast.Application(left, right, tree.function), max(lh, rh+1)
        elif isinstance(tree, ast.Variable):
            nonlocal var_num
            var_num += 1
        return tree, 1

    def compute(expr):
        if isinstance(expr, ast.Application):
            fn = {
                "+": "iadd",
                "-": "isub",
                "*": "imul",
                "/": "idiv",
            }[expr.function.symbol]
            compute(expr.left)
            compute(expr.right)

            result_program.append("    {}".format(fn))
        elif isinstance(expr, ast.Variable):
            result_program.append("    iload {}".format(variables[expr.name]))
        elif isinstance(expr, ast.Constant):
            c = expr.value
            if c <= 5:
                result_program.append("    iconst_{}".format(expr.value))
            else:
                result_program.append("    bipush {}".format(expr.value))
        else:
            raise Exception("no such node: {}".format(expr))

    stack_h = 0
    optprogram = []
    for decl in program:
        new_e, th = optimize(decl.expression)
        if isinstance(decl, ast.Assignment):
            newdecl = ast.Assignment(decl.variable, new_e)
        elif isinstance(decl, ast.Result):
            newdecl = ast.Result(new_e)
            th += 1
        else:
            raise Exception("no such TLD: {}".format(expr))
        optprogram.append(newdecl)
        stack_h = max(stack_h, th)

    result_program.append(".method public static main([Ljava/lang/String;)V")
    result_program.append(".limit stack {}".format(stack_h))
    result_program.append(".limit locals {}".format(var_num))

    for decl in optprogram:
        if isinstance(decl, ast.Assignment):
            compute(decl.expression)
            if decl.variable not in variables:
                variables[decl.variable] = var_counter
                var_counter+=1
            result_program.append("    istore {}".format(variables[decl.variable]))
        elif isinstance(decl, ast.Result):
            result_program.append("    getstatic  java/lang/System/out Ljava/io/PrintStream;")
            compute(decl.expression)
            result_program.append("    invokevirtual  java/io/PrintStream/println(I)V")
        else:
            raise Exception("no such TLD: {}".format(expr))

    result_program.append("    return")
    result_program.append(".end method")

    return "".join(e+"\n" for e in result_program)

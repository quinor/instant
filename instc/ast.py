from collections import namedtuple


Variable = namedtuple("Variable", ["name"])

Constant = namedtuple("Constant", ["value"])

Operator = namedtuple("Operator", ["symbol", "associativity", "precedence", "commutativeness"])

Application = namedtuple("Application", ["left", "right", "function"])

Assignment = namedtuple("Assignment", ["variable", "expression"])

Result = namedtuple("Result", ["expression"])

Add = Operator("+", "right", 1, True)
Sub = Operator("-", "left", 1, False)
Mul = Operator("*", "left", 2, True)
Div = Operator("/", "left", 2, False)


def traverse(tree, fn):
    fn(tree)
    if isinstance(tree, Application):
        traverse(tree.left, fn)
        traverse(tree.right, fn)

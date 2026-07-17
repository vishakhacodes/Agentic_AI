import ast
import operator as op
import math

OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.Mod: op.mod,
    ast.USub: op.neg,
}

FUNCTIONS = {
    "sqrt": math.sqrt,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "abs": abs,
    "round": round,
}


def execute(arguments: dict):
    expression = arguments.get("expression")

    if not expression:
        return "Calculator error: missing expression"

    try:
        tree = ast.parse(str(expression), mode="eval")
        value = _evaluate(tree.body)
        return str(value)
    except Exception as exc:
        return f"Calculator error: {exc}"


def _evaluate(node):
    if isinstance(node, ast.Constant):
        return node.value

    if isinstance(node, ast.BinOp):
        operator = OPERATORS[type(node.op)]
        return operator(_evaluate(node.left), _evaluate(node.right))

    if isinstance(node, ast.UnaryOp):
        operator = OPERATORS[type(node.op)]
        return operator(_evaluate(node.operand))

    if isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name):
            raise ValueError("Invalid function")

        func_name = node.func.id
        if func_name not in FUNCTIONS:
            raise ValueError(f"Unsupported function: {func_name}")

        args = [_evaluate(arg) for arg in node.args]
        return FUNCTIONS[func_name](*args)

    raise ValueError("Unsupported expression")

from enum import Enum, auto
from dataclasses import dataclass


class Operator(Enum):
    ADD = auto()
    SUB = auto()
    MULT = auto()
    DIV = auto()


class Node:
    pass


@dataclass
class BinaryExpr(Node):
    left: Node
    operator: Operator
    right: Node


@dataclass
class IntLiteral(Node):
    int_literal: int


@dataclass
class ParenExpr(Node):
    paren: Node


def calculate(expr):
    match expr:
        case IntLiteral():
            return expr.int_literal
        case BinaryExpr(operator=Operator.ADD):
            val_left = calculate(expr.left)
            val_right = calculate(expr.right)
            return val_left + val_right
        case BinaryExpr(operator=Operator.SUB):
            val_left = calculate(expr.left)
            val_right = calculate(expr.right)
            return val_left - val_right
        case BinaryExpr(operator=Operator.MULT):
            val_left = calculate(expr.left)
            val_right = calculate(expr.right)
            return val_left * val_right
        case BinaryExpr(operator=Operator.DIV):
            val_left = calculate(expr.left)
            val_right = calculate(expr.right)
            return val_left / val_right

def dump_ast(expr, level=0):
    indent_unit = "  "
    indentation = level * indent_unit
    match expr:
        case IntLiteral():
            return f"{indentation}{IntLiteral.__name__}({expr.int_literal})"
        case BinaryExpr():
            val_left = dump_ast(expr.left, level + 1)
            op = dump_ast(expr.operator, level + 1)
            val_right = dump_ast(expr.right, level + 1)
            return (f"{indentation}{BinaryExpr.__name__}"
                    f"\n{val_left}\n{op}\n{val_right}")
        case ParenExpr():
            paren = dump_ast(expr.paren, level + 1)
            return f"{indentation}{ParenExpr.__name__}\n{paren}"
        case Operator():
            return f"{indentation}{Operator.__name__}: {expr.name}"

tree = BinaryExpr(IntLiteral(1), Operator.ADD, BinaryExpr(IntLiteral(2), Operator.MULT, IntLiteral(3)))
print(dump_ast(tree))

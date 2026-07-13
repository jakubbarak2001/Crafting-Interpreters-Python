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
# 2 + 1
a = (BinaryExpr(IntLiteral(2), Operator.ADD, IntLiteral(1)))
print(calculate(a))

# def dump_ast(expr):
#     match expr:
#         case IntLiteral():
#             return f"{IntLiteral.__name__}({expr.int_literal})"
#         case BinaryExpr():
#             val_left = dump_ast(expr.left)
#             op = dump_ast(expr.operator)
#             val_right = dump_ast(expr.right)
#             return f"{BinaryExpr.__name__}\n  {val_left}\n  {op}\n  {val_right}"
#         case Operator(): # isinstance
#             return str(expr)
#         case ParenExpr():
#             return f"{ParenExpr.__name__}"

# tree = BinaryExpr(IntLiteral(1), Operator.ADD, BinaryExpr(IntLiteral(2), Operator.MULT, IntLiteral(3)))
# print(dump_ast(tree))


# 2     (4 + 8) * 2
# BinaryExpr
#   left: ParenExpr
#     expr: BinaryExpr
#       left: IntLiteral(4)
#       op: ADD
#       right: IntLiteral(8)
#   op: MUL
#   right: IntLiteral(2)

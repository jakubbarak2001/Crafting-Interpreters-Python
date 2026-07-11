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


b = BinaryExpr(IntLiteral(-2), Operator.SUB, IntLiteral(-2))
print(calculate(b))
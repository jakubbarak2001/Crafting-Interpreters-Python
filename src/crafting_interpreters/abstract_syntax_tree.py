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
class UnaryExpr(Node):
    operator: Operator
    operand: Node

@dataclass
class IntLiteral(Node):
    int_literal: int


@dataclass
class ParenExpr(Node):
    paren: Node


def calculate(expr: Node):
    match expr:
        case ParenExpr(inner):
            return calculate(inner)
        case IntLiteral(value):
            return value
        case BinaryExpr(left=left, operator=Operator.ADD, right=right):
            val_left, val_right = evaluate(left, right)
            return val_left + val_right
        case BinaryExpr(left=left, operator=Operator.SUB, right=right):
            val_left, val_right = evaluate(left, right)
            return val_left - val_right
        case BinaryExpr(left=left, operator=Operator.MULT, right=right):
            val_left, val_right = evaluate(left, right)
            return val_left * val_right
        case BinaryExpr(left=left, operator=Operator.DIV, right=right):
            val_left, val_right = evaluate(left, right)
            return val_left / val_right
        case UnaryExpr(operator=Operator.ADD, operand=operand):
            return calculate(operand)
        case UnaryExpr(operator=Operator.SUB, operand=operand):
            return -calculate(operand)

def evaluate(left: Node, right: Node):
    val_left = calculate(left)
    val_right = calculate(right)
    return val_left, val_right

def dump_ast(expr: Node | Operator, level:int=0):
    indent_unit = "  "
    indentation = level * indent_unit
    match expr:
        case IntLiteral(value):
            return f"{indentation}{IntLiteral.__name__}({value})"
        case BinaryExpr(left, operator, right):
            val_left = dump_ast(left, level + 1)
            op = dump_ast(operator, level + 1)
            val_right = dump_ast(right, level + 1)
            return (f"{indentation}{BinaryExpr.__name__}"
                    f"\n{val_left}\n{op}\n{val_right}")
        case UnaryExpr(operator, operand):
            val_operator = dump_ast(operator, level + 1)
            val_operand = dump_ast(operand, level + 1)
            return (f"{indentation}{UnaryExpr.__name__}"
                    f"\n{val_operator}\n{val_operand}")

        case ParenExpr(inner):
            paren = dump_ast(inner, level + 1)
            return f"{indentation}{ParenExpr.__name__}\n{paren}"
        case Operator(name=name):
            return f"{indentation}{Operator.__name__}: {name}"
        case _:
            raise ValueError(f"Unexpected input: {expr}")

# tree = BinaryExpr(ParenExpr(BinaryExpr(IntLiteral(2), Operator.MULT, IntLiteral(3))), Operator.ADD, IntLiteral(4))
# print(dump_ast(UnaryExpr(Operator.SUB, IntLiteral(1))))
# print(calculate(UnaryExpr(Operator.SUB, UnaryExpr(Operator.SUB, IntLiteral(1)))))
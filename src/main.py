from dataclasses import dataclass
from enum import Enum, auto

# if __name__ == '__main__':
#     token = tokenize("10 + 4")
#     print(token)
#     calculate(token)
#     print(token)

# expr := INT                   IntLiteral

# expr := expr PLUS expr        BinaryExpr
# expr := expr MINUS expr
# expr := expr STAR expr
# expr := expr SLASH expr

# expr := MINUS expr

# expr := LPAREN expr RPAREN


class BinaryOp(Enum):
    ADD = auto()
    SUB = auto()
    MUL = auto()
    DIV = auto()


@dataclass
class Expr:
    pass


@dataclass
class BinaryExpr(Expr):
    left: Expr
    op: BinaryOp
    right: Expr


@dataclass
class UnaryExpr(Expr):
    op: BinaryOp
    right: Expr


@dataclass
class IntLiteral(Expr):
    value: int


# ParenExpr
tree = BinaryExpr(IntLiteral(4), BinaryOp.ADD, IntLiteral(8))

# def calculate(expr: Expr) -> int:
#     match expr:
#         case BinaryExpr(l, BinaryOp.ADD, r):
#             return calculate(l) + calculate(r)
#         case IntLiteral(value):
#             return IntLiteral(value)
# case BinaryExpr(l, BinaryOp.SUB, r):
#     return calculate(l) - calculate(r)
# case BinaryExpr(l, BinaryOp.MUL, r):
#     return calculate(l) * calculate(r)
# case BinaryExpr(l, BinaryOp.DIV, r):
#     return calculate(l) / calculate(r)
# case UnaryExpr(BinaryOp.SUB, r)

print(calculate(tree))

# 2     (4 + 8) * 2
# BinaryExpr
#   left: ParenExpr
#     expr: BinaryExpr
#       left: IntLiteral(4)
#       op: ADD
#       right: IntLiteral(8)
#   op: MUL
#   right: IntLiteral(2)

# LIST (* (p (+ 4 8)) 2)


# 3*
# GraphViz
#     N1 [label="IntLit(4)"]
#     N2 [label="IntLit(8)"]
#     N3 [label="BinaryExpr(ADD)"]
#     N3 -> N1
#     N3 -> N2
# Abstract Syntax Tree

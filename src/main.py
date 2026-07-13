from dataclasses import dataclass
from enum import Enum, auto



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

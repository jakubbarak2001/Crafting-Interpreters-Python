from crafting_interpreters.abstract_syntax_tree import IntLiteral, Node, ParenExpr, dump_ast, Operator, BinaryExpr, \
    calculate, UnaryExpr
from crafting_interpreters.tokenizer import Token, tokenize, TokenKind

# Recursive descendant parsing
class Parser:
    def __init__(self, tokens: list[Token]):
        self._tokens = tokens
        self._current_token = 0

    # parse_expr := add_expr
    def parse_expr(self):
        return self.add_expr()

    #add_expr := mult_expr ((PLUS | MINUS) mult_expr)*
    def add_expr(self):
        e = self.mult_expr()
        while True:
            if self.peek() == TokenKind.PLUS:
                op = Operator.ADD
            elif self.peek() == TokenKind.MINUS:
                op = Operator.SUB
            else:
                return e
            self.consume()
            right = self.mult_expr()
            e = BinaryExpr(e, op, right)


    # mult_expr := unary_expr ((STAR | SLASH) unary_expr)*
    def mult_expr(self):
        e = self.unary_expr()
        while True:
            if self.peek() == TokenKind.STAR:
                op = Operator.MULT
            elif self.peek() == TokenKind.SLASH:
                op = Operator.DIV
            else:
                return e
            self.consume()
            right = self.unary_expr()
            e = BinaryExpr(e, op, right)

    # unary_expr := primary_expr
    def unary_expr(self):
        if self.peek() == TokenKind.PLUS or self.peek() == TokenKind.MINUS:
            operator_token = self.consume()
            if operator_token.kind == TokenKind.PLUS:
                operand = self.unary_expr()
                return operand
            elif operator_token.kind == TokenKind.MINUS:
                operator = Operator.NEG
                operand = self.unary_expr()
                return UnaryExpr(operator, operand) #UnaryExpr(Operator.SUB, IntLiteral(1))
        return self.primary_expr()

    # primary_expr := INT                   IntLiteral
    # primary_expr := LPAREN expr RPAREN
    def primary_expr(self) -> Node:
        match self.peek():
            case TokenKind.INT:
                t = self.consume()
                int_value = int(t.value)
                return IntLiteral(int_value)
            case TokenKind.LPAREN:
                self.consume()
                e = self.parse_expr()
                self.expect(TokenKind.RPAREN)
                return ParenExpr(e)
            case _:
                raise ValueError(f"Expected expression, but got {self.peek()}")

    def peek(self) -> TokenKind:
        return self._tokens[self._current_token].kind

    def consume(self) -> Token:
        t = self._tokens[self._current_token]
        self._current_token += 1
        return t

    def expect(self, kind: TokenKind) -> Token:
        if self.peek() != kind:
            raise ValueError(f"Expected {kind}, but got {self.peek()}")
        return self.consume()

# tokens = tokenize("-1")
# parse = Parser(tokens)
# expr = parse.parse_expr()
# print(calculate(expr))
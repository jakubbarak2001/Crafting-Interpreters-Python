from crafting_interpreters.abstract_syntax_tree import IntLiteral, Node, ParenExpr, dump_ast, Operator, BinaryExpr, \
    calculate
from crafting_interpreters.tokenizer import Token, tokenize, TokenKind

# Recursive descendant parsing
class Parser:
    def __init__(self, tokens: list[Token]):
        self._tokens = tokens
        self._current_token = 0

    # expr := add_expr
    def expr(self):
        return self.add_expr()

    # TODO: add_expr := mult_expr ((PLUS | MINUS) mult_expr)*
    def add_expr(self):
        return self.mult_expr()

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

    # TODO: unary_expr := MINUS unary_expr
    # unary_expr := primary_expr
    def unary_expr(self):
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
                e = self.expr()
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

tokens = tokenize("(42/2)")
parse = Parser(tokens)
expr = parse.expr()
print(calculate(expr))
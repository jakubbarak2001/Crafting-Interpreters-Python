import unittest
from crafting_interpreters.abstract_syntax_tree import (
    IntLiteral,
    BinaryExpr,
    calculate,
    Operator, dump_ast, ParenExpr, UnaryExpr,
)
from crafting_interpreters.parser import Parser
from crafting_interpreters.tokenizer import Token, TokenKind, tokenize


class TestArithmeticOperatorsScanning(unittest.TestCase):
    expected_output = [
        Token(TokenKind.PLUS, "+"),
        Token(TokenKind.MINUS, "-"),
        Token(TokenKind.STAR, "*"),
        Token(TokenKind.SLASH, "/"),
        Token(TokenKind.EOF, "")
    ]

    def test_standard_operators(self):
        self.assertEqual(tokenize("+-*/"), self.expected_output)

    def test_operators_with_whitespace(self):
        self.assertEqual(tokenize("   +  -   * /"), self.expected_output)

    def test_operators_invalid_character(self):
        self.assertRaises(ValueError, lambda: tokenize("$"))

    def test_comment_is_skipped(self):
        self.assertEqual(
            tokenize("+ # this is ignored\n-"),
            [Token(TokenKind.PLUS, "+"), Token(TokenKind.MINUS, "-"), Token(TokenKind.EOF, "")],
        )

    def test_comment_at_end_of_file(self):
        self.assertEqual(tokenize("+ # this is ignored"), [Token(TokenKind.PLUS, "+"), Token(TokenKind.EOF, "")])

    def test_newline_is_whitespace(self):
        self.assertEqual(
            tokenize("+\n-"),
            [Token(TokenKind.PLUS, "+"), Token(TokenKind.MINUS, "-"), Token(TokenKind.EOF, "")],
        )


class TestComparisonOperatorsScanning(unittest.TestCase):
    def test_comparison_operators(self):
        self.assertEqual(
            tokenize("< > ="),
            [
                Token(TokenKind.LT, "<"),
                Token(TokenKind.GT, ">"),
                Token(TokenKind.EQ, "="),
                Token(TokenKind.EOF, ""),
            ],
        )

    def test_maximal_munch(self):
        self.assertEqual(
            tokenize("<= >= == !="),
            [
                Token(TokenKind.LT_EQ, "<="),
                Token(TokenKind.GT_EQ, ">="),
                Token(TokenKind.EQ_EQ, "=="),
                Token(TokenKind.BANG_EQ, "!="),
                Token(TokenKind.EOF, ""),
            ],
        )

    def test_maximal_munch_rule(self):
        self.assertEqual(
            tokenize("<== >== ==="),
            [
                Token(TokenKind.LT_EQ, "<="),
                Token(TokenKind.EQ, "="),
                Token(TokenKind.GT_EQ, ">="),
                Token(TokenKind.EQ, "="),
                Token(TokenKind.EQ_EQ, "=="),
                Token(TokenKind.EQ, "="),
                Token(TokenKind.EOF, ""),
            ],
        )


class TestASTArithmeticCalculation(unittest.TestCase):
    def test_calculate_int_literal(self):
        tree = IntLiteral(10)
        self.assertEqual(calculate(tree), 10)

    def test_calculate_binary_expr_add(self):
        tree = BinaryExpr(IntLiteral(1), Operator.ADD, IntLiteral(2))
        self.assertEqual(calculate(tree), 3)

    def test_calculate_binary_expr_sub(self):
        tree = BinaryExpr(IntLiteral(3), Operator.SUB, IntLiteral(2))
        self.assertEqual(calculate(tree), 1)

    def test_calculate_binary_expr_sub_negative_left(self):
        tree = BinaryExpr(IntLiteral(-2), Operator.SUB, IntLiteral(2))
        self.assertEqual(calculate(tree), -4)

    def test_calculate_binary_expr_sub_negative_right(self):
        tree = BinaryExpr(IntLiteral(2), Operator.SUB, IntLiteral(-2))
        self.assertEqual(calculate(tree), 4)

    def test_calculate_binary_expr_sub_negative_both(self):
        tree = BinaryExpr(IntLiteral(-2), Operator.SUB, IntLiteral(-2))
        self.assertEqual(calculate(tree), 0)

    def test_calculate_binary_expr_mult(self):
        tree = BinaryExpr(IntLiteral(5), Operator.MULT, IntLiteral(2))
        self.assertEqual(calculate(tree), 10)

    def test_calculate_binary_expr_div_int(self):
        tree = BinaryExpr(IntLiteral(4), Operator.DIV, IntLiteral(2))
        self.assertEqual(calculate(tree), 2)

    def test_calculate_binary_expr_div_float(self):
        tree = BinaryExpr(IntLiteral(5), Operator.DIV, IntLiteral(2))
        self.assertEqual(calculate(tree), 2.5)

    def test_calculate_binary_expr_div_zero(self):
        tree = BinaryExpr(IntLiteral(5), Operator.DIV, IntLiteral(0))

        with self.assertRaises(ZeroDivisionError):
            calculate(tree)

    def test_calculate_unary_expr(self):
        tree = UnaryExpr(Operator.NEG, IntLiteral(1))
        self.assertEqual(calculate(tree), -1)

    def test_calculate_unary_expr_double_minus(self):
        tree = UnaryExpr(Operator.NEG, UnaryExpr(Operator.NEG, IntLiteral(1)))
        self.assertEqual(calculate(tree), 1)

class TestASTStructure(unittest.TestCase):
    def test_int_literal_payload(self):
         tree = IntLiteral(10)
         self.assertEqual(dump_ast(tree), "IntLiteral(10)")

    def test_int_literal_indentation(self):
        tree = IntLiteral(10)
        self.assertEqual(dump_ast(tree, 2), "    IntLiteral(10)")

    def test_binary_expr_payload(self):
        tree = BinaryExpr(IntLiteral(1), Operator.ADD, IntLiteral(2))
        self.assertEqual(dump_ast(tree), "BinaryExpr"
                                         "\n  IntLiteral(1)"
                                         "\n  Operator: ADD"
                                         "\n  IntLiteral(2)")

    def test_binary_expr_payload_nested(self):
        tree = BinaryExpr(IntLiteral(1), Operator.ADD, BinaryExpr(IntLiteral(2), Operator.MULT, IntLiteral(3)))
        self.assertEqual(dump_ast(tree), "BinaryExpr"
                                         "\n  IntLiteral(1)"
                                         "\n  Operator: ADD"
                                         "\n  BinaryExpr"
                                         "\n    IntLiteral(2)"
                                         "\n    Operator: MULT"
                                         "\n    IntLiteral(3)")

    def test_paren_expr_payload(self):
        tree = BinaryExpr(IntLiteral(1), Operator.MULT, ParenExpr(BinaryExpr(IntLiteral(2), Operator.ADD, IntLiteral(3))))
        self.assertEqual(dump_ast(tree), "BinaryExpr"
                                         "\n  IntLiteral(1)"
                                         "\n  Operator: MULT"
                                         "\n  ParenExpr"
                                         "\n    BinaryExpr"
                                         "\n      IntLiteral(2)"
                                         "\n      Operator: ADD"
                                         "\n      IntLiteral(3)")

    def test_unary_minus(self):
        tree = BinaryExpr(UnaryExpr(Operator.SUB, IntLiteral(5)), Operator.MULT, IntLiteral(2))
        self.assertEqual(dump_ast(tree), "BinaryExpr"
                                         "\n  UnaryExpr"
                                         "\n    Operator: SUB"
                                         "\n    IntLiteral(5)"
                                         "\n  Operator: MULT"
                                         "\n  IntLiteral(2)")

    def test_unary_nested_minus(self):
        tree = BinaryExpr(UnaryExpr(Operator.SUB, UnaryExpr(Operator.SUB, IntLiteral(5))), Operator.MULT, IntLiteral(2))
        self.assertEqual(dump_ast(tree), "BinaryExpr"
                                         "\n  UnaryExpr"
                                         "\n    Operator: SUB"
                                         "\n    UnaryExpr"
                                         "\n      Operator: SUB"
                                         "\n      IntLiteral(5)"
                                         "\n  Operator: MULT"
                                         "\n  IntLiteral(2)")

class TestParserArithmetic(unittest.TestCase):
    def create_value_for_pipeline(self, val:str):
        self.value = val
        tokens = tokenize(val)
        parse = Parser(tokens)
        expr = parse.parse_expr()
        calculated_value = calculate(expr)
        return calculated_value

    def test_token_to_calculate_pipeline(self):
        expr_value = self.create_value_for_pipeline("20/10")
        self.assertEqual(expr_value, 2.0)

    def test_add_expr(self):
        expr_value = self.create_value_for_pipeline("10+5")
        self.assertEqual(expr_value, 15.0)

    def test_precedence_level(self):
        expr_value = self.create_value_for_pipeline("1+2*3")
        self.assertEqual(expr_value, 7.0)

    def test_unary_expr(self):
        expr_value = self.create_value_for_pipeline("-1")
        self.assertEqual(expr_value, -1)

if __name__ == "__main__":
    unittest.main()

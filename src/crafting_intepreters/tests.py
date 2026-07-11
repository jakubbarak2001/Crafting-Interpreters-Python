import unittest
from crafting_intepreters.abstract_syntax_tree import (
    IntLiteral,
    BinaryExpr,
    calculate,
    Operator,
)
from crafting_intepreters.tokenizer import Token, TokenKind, tokenize


class TestArithmeticOperatorsScanning(unittest.TestCase):
    expected_output = [
        Token(TokenKind.PLUS, "+"),
        Token(TokenKind.MINUS, "-"),
        Token(TokenKind.STAR, "*"),
        Token(TokenKind.SLASH, "/"),
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
            [Token(TokenKind.PLUS, "+"), Token(TokenKind.MINUS, "-")],
        )

    def test_comment_at_end_of_file(self):
        self.assertEqual(tokenize("+ # this is ignored"), [Token(TokenKind.PLUS, "+")])

    def test_newline_is_whitespace(self):
        self.assertEqual(
            tokenize("+\n-"),
            [Token(TokenKind.PLUS, "+"), Token(TokenKind.MINUS, "-")],
        )


class TestComparisonOperatorsScanning(unittest.TestCase):
    def test_comparison_operators(self):
        self.assertEqual(
            tokenize("< > ="),
            [
                Token(TokenKind.LT, "<"),
                Token(TokenKind.GT, ">"),
                Token(TokenKind.EQ, "="),
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


if __name__ == "__main__":
    unittest.main()

import unittest
from crafting_intepreters.tokenizer import Token, TokenKind, tokenize

class TestArithmeticOperatorsScanning(unittest.TestCase):
    expected_output = [
        Token(TokenKind.PLUS, '+'),
        Token(TokenKind.MINUS, '-'),
        Token(TokenKind.STAR, '*'),
        Token(TokenKind.SLASH, '/'),
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
            [Token(TokenKind.PLUS, '+'), Token(TokenKind.MINUS, '-')],
        )
    def test_comment_at_end_of_file(self):
        self.assertEqual(
            tokenize("+ # this is ignored"),
            [Token(TokenKind.PLUS, '+')]
        )

    def test_newline_is_whitespace(self):
        self.assertEqual(
            tokenize("+\n-"),
            [Token(TokenKind.PLUS, '+'), Token(TokenKind.MINUS, '-')],
        )


class TestComparisonOperatorsScanning(unittest.TestCase):
    def test_comparison_operators(self):
        self.assertEqual(
            tokenize("< > ="),
            [Token(TokenKind.LT, '<'), Token(TokenKind.GT, '>'), Token(TokenKind.EQ, '=')]
        )

    def test_maximal_munch(self):
        self.assertEqual(
            tokenize("<= >= == !="),
            [Token(TokenKind.LT_EQ, '<='), Token(TokenKind.GT_EQ, '>='),
             Token(TokenKind.EQ_EQ, '=='), Token(TokenKind.BANG_EQ, '!=')]
        )

    def test_maximal_munch_rule(self):
        self.assertEqual(
            tokenize("<== >== ==="),
            [Token(TokenKind.LT_EQ, '<='), Token(TokenKind.EQ, '='),
             Token(TokenKind.GT_EQ, '>='), Token(TokenKind.EQ, '='),
             Token(TokenKind.EQ_EQ, '=='), Token(TokenKind.EQ, '=')]
        )


if __name__ == '__main__':
    unittest.main()


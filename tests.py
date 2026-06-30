import unittest
from main import tokenize, Token, TokenKind

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


if __name__ == '__main__':
    unittest.main()


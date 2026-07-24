from dataclasses import dataclass
from enum import Enum, auto

class TokenKind(Enum):
    INT = auto()
    LPAREN = auto()
    RPAREN = auto()
    EOF = auto()
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    WHITESPACE = auto()
    COMMENT = auto()
    EQ = auto()
    LT = auto()
    LT_EQ = auto()
    GT = auto()
    GT_EQ = auto()
    EQ_EQ = auto()
    BANG = auto()
    BANG_EQ = auto()
    IDENTIFIER = auto()
    PRINT = auto()
    SEMICOLON = auto()

KEYWORDS = {
      "print": TokenKind.PRINT,
  }

@dataclass(frozen=True)
class Token:
    kind: TokenKind
    value: str

    def __repr__(self):
        return f"{self.kind.name} {self.value!r}"

def _is_digit(c: str) -> bool:
    return "0" <= c <= "9"

def _is_alpha(c: str) -> bool:
    return _is_lower_alpha(c) or _is_upper_alpha(c)

def _is_upper_alpha(c: str) -> bool:
    return "A" <= c <= "Z"

def _is_lower_alpha(c: str) -> bool:
    return "a" <= c <= "z"

def _is_first_id_letter(c: str) -> bool:
    return _is_alpha(c) or c == "_"

def _is_other_id_letter(c: str) -> bool:
    return _is_alpha(c) or c == "_" or _is_digit(c)

class CharStream:
    def __init__(self, src: str):
        self._src = src
        self._pos = 0
        self._start = 0

    def mark_start(self):
        self._start = self._pos

    def mark_end(self) -> str:
        return self._src[self._start : self._pos]

    def next(self) -> str:
        if (c := self.peek()) != "":
            self._pos += 1
        return c

    def peek(self) -> str:
        return self._src[self._pos] if self._pos < len(self._src) else ""
        # if self._pos < len(self._src):
        #     return self._src[self._pos]
        # else:
        #     return ''

def _parse_one_token(stream: CharStream) -> TokenKind:
    match stream.next():
        case "(":
            return TokenKind.LPAREN
        case ")":
            return TokenKind.RPAREN
        case "+":
            return TokenKind.PLUS
        case "-":
            return TokenKind.MINUS
        case "/":
            return TokenKind.SLASH
        case "*":
            return TokenKind.STAR
        case "#":
            while stream.peek() != "\n" and stream.peek() != "":
                stream.next()
            return TokenKind.COMMENT
        case c if _is_digit(c):
            while _is_digit(stream.peek()):
                stream.next()
            return TokenKind.INT
        case c if _is_first_id_letter(c):
            while _is_other_id_letter(stream.peek()):
                stream.next()
            return TokenKind.IDENTIFIER
        case ";":
            return TokenKind.SEMICOLON
        case " " | "\n":
            return TokenKind.WHITESPACE
        case "<":
            if stream.peek() == "=":
                stream.next()
                return TokenKind.LT_EQ
            else:
                return TokenKind.LT
        case ">":
            if stream.peek() == "=":
                stream.next()
                return TokenKind.GT_EQ
            else:
                return TokenKind.GT
        case "=":
            if stream.peek() == "=":
                stream.next()
                return TokenKind.EQ_EQ
            else:
                return TokenKind.EQ
        case "!":
            if stream.peek() == "=":
                stream.next()
                return TokenKind.BANG_EQ
            else:
                return TokenKind.BANG
        case c:
            raise ValueError(f"Invalid symbol: {c}")

def tokenize(src: str) -> list[Token]:
    tokens = []
    stream = CharStream(src)
    while stream.peek() != "":
        stream.mark_start()
        token_kind = _parse_one_token(stream)
        token_value = stream.mark_end()

        if token_kind == TokenKind.IDENTIFIER:
            token_kind = KEYWORDS.get(token_value, TokenKind.IDENTIFIER)

        if token_kind not in (TokenKind.WHITESPACE, TokenKind.COMMENT):
            tokens.append(Token(token_kind, token_value))

    tokens.append(Token(TokenKind.EOF, ""))
    return tokens

# print(tokenize("print 1 + 2;"))

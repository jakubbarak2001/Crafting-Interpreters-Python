from dataclasses import dataclass
from enum import Enum, auto

class TokenKind(Enum):
    INT = auto()
    LPAREN = auto()
    RPAREN = auto()
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    WHITESPACE = auto()
    COMMENT = auto()


@dataclass(frozen=True)
class Token:
    kind: TokenKind
    value: str


def _is_digit(c: str) -> bool:
    return '0' <= c <= '9'


class CharStream:
    def __init__(self, src: str):
        self._src = src
        self._pos = 0
        self._start = 0

    def mark_start(self):
        self._start = self._pos

    def mark_end(self) -> str:
        return self._src[self._start:self._pos]

    def next(self) -> str:
        if (c := self.peek()) != '':
            self._pos += 1
        return c

    def peek(self) -> str:
        return self._src[self._pos] if self._pos < len(self._src) else ''
        # if self._pos < len(self._src):
        #     return self._src[self._pos]
        # else:
        #     return ''


def _parse_one_token(stream: CharStream) -> TokenKind:
    match stream.next():
        case '(':
            return TokenKind.LPAREN
        case ')':
            return TokenKind.RPAREN
        case '+':
            return TokenKind.PLUS
        case '-':
            return TokenKind.MINUS
        case '/':
            return TokenKind.SLASH
        case '*':
            return TokenKind.STAR
        case '#':
            while stream.peek() != '\n' and stream.peek() != '':
                stream.next()
            return TokenKind.COMMENT
        case c if _is_digit(c):
            while _is_digit(stream.peek()):
                stream.next()
            return TokenKind.INT
        case ' ' | '\n':
            return TokenKind.WHITESPACE
        case c:
            raise ValueError(f'Invalid symbol: {c}')


def tokenize(src: str) -> list[Token]:
    tokens = []
    stream = CharStream(src)
    while stream.peek() != '':
        stream.mark_start()
        token_kind = _parse_one_token(stream)
        if token_kind not in (TokenKind.WHITESPACE, TokenKind.COMMENT):
            tokens.append(Token(token_kind, stream.mark_end()))
    return tokens

if __name__ == '__main__':
    token = tokenize("  4 2+  ###312312 ")
    print(token)

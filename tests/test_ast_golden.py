import pytest

from crafting_interpreters.abstract_syntax_tree import dump_ast
from crafting_interpreters.parser import Parser
from crafting_interpreters.tokenizer import tokenize


CASES = [
    pytest.param("precedence", "1 + 2 * 3", id="precedence"),
    pytest.param("parentheses", "(1 + 2) * 3", id="parentheses"),
    pytest.param("unary", "--5 * 2", id="unary"),
]


@pytest.mark.parametrize(("name", "source"), CASES)
def test_expression_ast(name, source, file_regression):
    tree = Parser(tokenize(source)).parse_expr()
    rendered = f"source: {source}\n\n{dump_ast(tree)}\n"

    file_regression.check(
        rendered,
        basename=name,
        extension=".ast",
    )

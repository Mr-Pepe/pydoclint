"""Tests for the violations.Error class."""


import astroid
import pytest

from pydocstyle.docstring_error import DocstringError

FUNCTION_CODE = """def my_func() -> None:
        ...
    """

CLASS_CODE = """class MyClass:
        ...
    """

module_node = astroid.parse(
    code=f"\n{FUNCTION_CODE}\n\n{CLASS_CODE}",
    module_name="my_module",
    path="/path/to/my/file",
)

function_node = list(module_node.get_children())[0]
class_node = list(module_node.get_children())[1]


class MyError(DocstringError):
    error_code = "D123"
    description = "some short description"


def test_file_name() -> None:
    error = MyError(module_node)

    assert error.file_name == "/path/to/my/file"


def test_line() -> None:
    error = MyError(function_node)

    assert error.line == 2


def test_node_name() -> None:
    error = MyError(function_node)

    assert error.node_name == "my_func"


def test_print_for_function_node() -> None:
    error = MyError(function_node)

    assert (
        str(error)
        == "/path/to/my/file:2 in function 'my_func': D123 - some short description"
    )


def test_print_for_module_node() -> None:
    error = MyError(module_node)

    assert (
        str(error)
        == "/path/to/my/file:0 in module 'my_module': D123 - some short description"
    )


def test_print_for_class_node() -> None:
    error = MyError(class_node)

    assert (
        str(error)
        == "/path/to/my/file:6 in class 'MyClass': D123 - some short description"
    )


def test_str_and_repr() -> None:
    error = MyError(class_node)

    assert str(error) == error.__repr__()

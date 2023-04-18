"""Contains a check for proper capitalization of the summary line."""

import ast
import string
from typing import Optional

from astroid import FunctionDef

from pydocstyle._config import Configuration
from pydocstyle._docstring import Docstring
from pydocstyle._docstring_error import D403
from pydocstyle.checks import check


@check(FunctionDef)
def check_capitalized(_: FunctionDef, docstring: Docstring, __: Configuration) -> Optional[D403]:
    """D403: First word of the first line should be properly capitalized."""
    first_word: str = docstring.content.split()[0]

    if first_word in (first_word.upper(), first_word.capitalize()):
        return None

    if first_word.startswith("'"):
        return None

    for char in first_word:
        if char not in string.ascii_letters and char != "'":
            return None

    return D403(first_word.capitalize(), first_word)
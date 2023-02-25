from typing import Generator, List, Tuple, Union

from astroid import NodeNG

from pydocstyle.checks import check
from pydocstyle.config import Configuration
from pydocstyle.docstring import Docstring
from pydocstyle.utils import get_indents, has_content, leading_space, pairwise
from pydocstyle.violations import D206, D207, D208


@check(NodeNG)
def check_indentation(
    node: NodeNG, docstring: Docstring, config: Configuration
) -> Generator[Union[D206, D207, D208], None, None]:
    """D206, D207, D208: The entire docstring should be indented same as code.

    The entire docstring is indented the same as the quotes at its
    first line without using tabs.
    """
    if not docstring:
        return None

    docstring_indent, line_indents = get_indents(node, docstring)

    if len(line_indents) == 0:
        return None

    if "\t" in docstring_indent or any(
        "\t" in line_indent for line_indent in line_indents
    ):
        yield D206()

    if (
        len(line_indents) > 1 and min(line_indents[:-1]) > docstring_indent
    ) or line_indents[-1] > docstring_indent:
        yield D208()

    if min(line_indents) < docstring_indent:
        yield D207()

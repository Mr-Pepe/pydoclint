import importlib
import inspect
import pkgutil
from types import ModuleType
from typing import Generator, Iterator, List, Type

import pydocstyle.checks
from pydocstyle import DocstringError


def get_checks() -> List[Type[DocstringError]]:
    """Discovers docstring checks in the 'pydocstyle.checks' namespace."""
    errors: List[DocstringError] = []

    for _, module_name, _ in _iter_namespace(pydocstyle.checks):
        module = importlib.import_module(module_name)

        errors.extend(_get_checks_from_module(module))

    return errors


def _iter_namespace(ns_pkg: ModuleType) -> Iterator[pkgutil.ModuleInfo]:
    """Iterates over the modules in a given package namespace."""
    return pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + ".")


def _get_checks_from_module(
    module: ModuleType,
) -> Generator[Type[DocstringError], None, None]:
    for member in dir(module):
        candidate = getattr(module, member)
        if (
            inspect.isclass(candidate)
            and issubclass(candidate, DocstringError)
            and not candidate == DocstringError
        ):
            yield candidate

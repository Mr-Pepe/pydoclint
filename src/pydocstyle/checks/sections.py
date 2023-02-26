# from pydocstyle.checks import check


# def _is_docstring_section(context):
#     """Check if the suspected context is really a section header.

#     Lets have a look at the following example docstring:
#         '''Title.

#         Some part of the docstring that specifies what the function
#         returns. <----- Not a real section name. It has a suffix and the
#                         previous line is not empty and does not end with
#                         a punctuation sign.

#         This is another line in the docstring. It describes stuff,
#         but we forgot to add a blank line between it and the section name.
#         Parameters  <-- A real section name. The previous line ends with
#         ----------      a period, therefore it is in a new
#                         grammatical context.
#         param : int
#         examples : list  <------- Not a section - previous line doesn't end
#             A list of examples.   with punctuation.
#         notes : list  <---------- Not a section - there's text after the
#             A list of notes.      colon.

#         Notes:  <--- Suspected as a context because there's a suffix to the
#         -----        section, but it's a colon so it's probably a mistake.
#         Bla.

#         '''

#     To make sure this is really a section we check these conditions:
#         * There's no suffix to the section name or it's just a colon AND
#         * The previous line is empty OR it ends with punctuation.

#     If one of the conditions is true, we will consider the line as
#     a section name.
#     """
#     section_name_suffix = (
#         context.line.strip().lstrip(context.section_name.strip()).strip()
#     )

#     section_suffix_is_only_colon = section_name_suffix == ':'

#     punctuation = [',', ';', '.', '-', '\\', '/', ']', '}', ')']
#     prev_line_ends_with_punctuation = any(
#         context.previous_line.strip().endswith(x) for x in punctuation
#     )

#     this_line_looks_like_a_section_name = (
#         is_blank(section_name_suffix) or section_suffix_is_only_colon
#     )

#     prev_line_looks_like_end_of_paragraph = (
#         prev_line_ends_with_punctuation or is_blank(context.previous_line)
#     )

#     return (
#         this_line_looks_like_a_section_name
#         and prev_line_looks_like_end_of_paragraph
#     )


# @classmethod
# def _check_blanks_and_section_underline(
#     cls, section_name, context, indentation
# ):
#     """D4{07,08,09,12,14}, D215: Section underline checks.

#     Check for correct formatting for docstring sections. Checks that:
#         * The line that follows the section name contains
#             dashes (D40{7,8}).
#         * The amount of dashes is equal to the length of the section
#             name (D409).
#         * The section's content does not begin in the line that follows
#             the section header (D412).
#         * The section has no content (D414).
#         * The indentation of the dashed line is equal to the docstring's
#             indentation (D215).
#     """
#     blank_lines_after_header = 0

#     for line in context.following_lines:
#         if not is_blank(line):
#             break
#         blank_lines_after_header += 1
#     else:
#         # There are only blank lines after the header.
#         yield violations.D407(section_name)
#         yield violations.D414(section_name)
#         return

#     non_empty_line = context.following_lines[blank_lines_after_header]
#     dash_line_found = ''.join(set(non_empty_line.strip())) == '-'

#     if not dash_line_found:
#         yield violations.D407(section_name)
#         if blank_lines_after_header > 0:
#             yield violations.D412(section_name)
#     else:
#         if blank_lines_after_header > 0:
#             yield violations.D408(section_name)

#         if non_empty_line.strip() != "-" * len(section_name):
#             yield violations.D409(
#                 len(section_name),
#                 section_name,
#                 len(non_empty_line.strip()),
#             )

#         if leading_space(non_empty_line) > indentation:
#             yield violations.D215(section_name)

#         line_after_dashes_index = blank_lines_after_header + 1
#         # If the line index after the dashes is in range (perhaps we have
#         # a header + underline followed by another section header).
#         if line_after_dashes_index < len(context.following_lines):
#             line_after_dashes = context.following_lines[
#                 line_after_dashes_index
#             ]
#             if is_blank(line_after_dashes):
#                 rest_of_lines = context.following_lines[
#                     line_after_dashes_index:
#                 ]
#                 if not is_blank(''.join(rest_of_lines)):
#                     yield violations.D412(section_name)
#                 else:
#                     yield violations.D414(section_name)
#         else:
#             yield violations.D414(section_name)


# @classmethod
# def _check_common_section(
#     cls, docstring, definition, context, valid_section_names
# ):
#     """D4{05,10,11,13}, D214: Section name checks.

#     Check for valid section names. Checks that:
#         * The section name is properly capitalized (D405).
#         * The section is not over-indented (D214).
#         * There's a blank line after the section (D410, D413).
#         * There's a blank line before the section (D411).

#     Also yields all the errors from `_check_blanks_and_section_underline`.
#     """
#     indentation, _ = get_indents(definition, docstring)
#     capitalized_section = context.section_name.title()

#     if (
#         context.section_name not in valid_section_names
#         and capitalized_section in valid_section_names
#     ):
#         yield violations.D405(capitalized_section, context.section_name)

#     if leading_space(context.line) > indentation:
#         yield violations.D214(capitalized_section)

#     if not context.following_lines or not is_blank(
#         context.following_lines[-1]
#     ):
#         if context.is_last_section:
#             yield violations.D413(capitalized_section)
#         else:
#             yield violations.D410(capitalized_section)

#     if not is_blank(context.previous_line):
#         yield violations.D411(capitalized_section)

#     yield from cls._check_blanks_and_section_underline(
#         capitalized_section, context, indentation
#     )


# @classmethod
# def _check_numpy_section(cls, docstring, definition, context):
#     """D406: NumPy-style section name checks.

#     Check for valid section names. Checks that:
#         * The section name has no superfluous suffix to it (D406).

#     Additionally, also yield all violations from `_check_common_section`
#     which are style-agnostic section checks.
#     """
#     indentation, _ = get_indents(definition, docstring)
#     capitalized_section = context.section_name.title()
#     yield from cls._check_common_section(
#         docstring, definition, context, cls.NUMPY_SECTION_NAMES
#     )
#     suffix = context.line.strip().lstrip(context.section_name)
#     if suffix:
#         yield violations.D406(capitalized_section, context.line.strip())

#     if capitalized_section == "Parameters":
#         yield from cls._check_parameters_section(
#             docstring, definition, context
#         )


# @staticmethod
# def _check_parameters_section(docstring, definition, context):
#     """D417: `Parameters` section check for numpy style.

#     Check for a valid `Parameters` section. Checks that:
#         * The section documents all function arguments (D417)
#             except `self` or `cls` if it is a method.

#     """
#     docstring_args = set()
#     section_level_indent = leading_space(context.line)
#     # Join line continuations, then resplit by line.
#     content = (
#         '\n'.join(context.following_lines).replace('\\\n', '').split('\n')
#     )
#     for current_line, next_line in zip(content, content[1:]):
#         # All parameter definitions in the Numpy parameters
#         # section must be at the same indent level as the section
#         # name.
#         # Also, we ensure that the following line is indented,
#         # and has some string, to ensure that the parameter actually
#         # has a description.
#         # This means, this is a parameter doc with some description
#         if (
#             (leading_space(current_line) == section_level_indent)
#             and (
#                 len(leading_space(next_line))
#                 > len(leading_space(current_line))
#             )
#             and next_line.strip()
#         ):
#             # In case the parameter has type definitions, it
#             # will have a colon
#             if ":" in current_line:
#                 parameters, parameter_type = current_line.split(":", 1)
#             # Else, we simply have the list of parameters defined
#             # on the current line.
#             else:
#                 parameters = current_line.strip()
#             # Numpy allows grouping of multiple parameters of same
#             # type in the same line. They are comma separated.
#             parameter_list = parameters.split(",")
#             for parameter in parameter_list:
#                 docstring_args.add(parameter.strip())
#     yield from ConventionChecker._check_missing_args(
#         docstring_args, definition
#     )


# @staticmethod
# def _check_args_section(docstring, definition, context):
#     """D417: `Args` section checks.

#     Check for a valid `Args` or `Argument` section. Checks that:
#         * The section documents all function arguments (D417)
#             except `self` or `cls` if it is a method.

#     Documentation for each arg should start at the same indentation
#     level. For example, in this case x and y are distinguishable::

#         Args:
#             x: Lorem ipsum dolor sit amet
#             y: Ut enim ad minim veniam

#     In the case below, we only recognize x as a documented parameter
#     because the rest of the content is indented as if it belongs
#     to the description for x::

#         Args:
#             x: Lorem ipsum dolor sit amet
#                 y: Ut enim ad minim veniam
#     """
#     docstring_args = set()

#     # normalize leading whitespace
#     if context.following_lines:
#         # any lines with shorter indent than the first one should be disregarded
#         first_line = context.following_lines[0]
#         leading_whitespaces = first_line[: -len(first_line.lstrip())]

#     args_content = dedent(
#         "\n".join(
#             [
#                 line
#                 for line in context.following_lines
#                 if line.startswith(leading_whitespaces) or line == ""
#             ]
#         )
#     ).strip()

#     args_sections = []
#     for line in args_content.splitlines(keepends=True):
#         if not line[:1].isspace():
#             # This line is the start of documentation for the next
#             # parameter because it doesn't start with any whitespace.
#             args_sections.append(line)
#         else:
#             # This is a continuation of documentation for the last
#             # parameter because it does start with whitespace.
#             args_sections[-1] += line

#     for section in args_sections:
#         match = ConventionChecker.GOOGLE_ARGS_REGEX.match(section)
#         if match:
#             docstring_args.add(match.group(1))
#     yield from ConventionChecker._check_missing_args(
#         docstring_args, definition
#     )


# @staticmethod
# def _check_missing_args(docstring_args, definition):
#     """D417: Yield error for missing arguments in docstring.

#     Given a list of arguments found in the docstring and the
#     callable definition, it checks if all the arguments of the
#     callable are present in the docstring, else it yields a
#     D417 with a list of missing arguments.

#     """
#     if isinstance(definition, Function):
#         function_args = get_function_args(definition.source)
#         # If the method isn't static, then we skip the first
#         # positional argument as it is `cls` or `self`
#         if definition.kind == 'method' and not definition.is_static:
#             function_args = function_args[1:]
#         # Filtering out any arguments prefixed with `_` marking them
#         # as private.
#         function_args = [
#             arg_name
#             for arg_name in function_args
#             if not is_def_arg_private(arg_name)
#         ]
#         missing_args = set(function_args) - docstring_args
#         if missing_args:
#             yield violations.D417(
#                 ", ".join(sorted(missing_args)), definition.name
#             )


# @classmethod
# def _check_google_section(cls, docstring, definition, context):
#     """D416: Google-style section name checks.

#     Check for valid section names. Checks that:
#         * The section does not contain any blank line between its name
#             and content (D412).
#         * The section is not empty (D414).
#         * The section name has colon as a suffix (D416).

#     Additionally, also yield all violations from `_check_common_section`
#     which are style-agnostic section checks.
#     """
#     capitalized_section = context.section_name.title()
#     yield from cls._check_common_section(
#         docstring, definition, context, cls.GOOGLE_SECTION_NAMES
#     )
#     suffix = context.line.strip().lstrip(context.section_name)
#     if suffix != ":":
#         yield violations.D416(capitalized_section + ":", context.line.strip())

#     if capitalized_section in ("Args", "Arguments"):
#         yield from cls._check_args_section(docstring, definition, context)


# @staticmethod
# def _get_section_contexts(lines, valid_section_names):
#     """Generate `SectionContext` objects for valid sections.

#     Given a list of `valid_section_names`, generate an
#     `Iterable[SectionContext]` which provides:
#         * Section Name
#         * String value of the previous line
#         * The section line
#         * Following lines till the next section
#         * Line index of the beginning of the section in the docstring
#         * Boolean indicating whether the section is the last section.
#     for each valid section.

#     """
#     lower_section_names = [s.lower() for s in valid_section_names]

#     def _suspected_as_section(_line):
#         result = get_leading_words(_line.lower())
#         return result in lower_section_names

#     # Finding our suspects.
#     suspected_section_indices = [
#         i for i, line in enumerate(lines) if _suspected_as_section(line)
#     ]

#     SectionContext = namedtuple(
#         'SectionContext',
#         (
#             'section_name',
#             'previous_line',
#             'line',
#             'following_lines',
#             'original_index',
#             'is_last_section',
#         ),
#     )

#     # First - create a list of possible contexts. Note that the
#     # `following_lines` member is until the end of the docstring.
#     contexts = (
#         SectionContext(
#             get_leading_words(lines[i].strip()),
#             lines[i - 1],
#             lines[i],
#             lines[i + 1 :],
#             i,
#             False,
#         )
#         for i in suspected_section_indices
#     )

#     # Now that we have manageable objects - rule out false positives.
#     contexts = (
#         c for c in contexts if ConventionChecker._is_docstring_section(c)
#     )

#     # Now we shall trim the `following lines` field to only reach the
#     # next section name.
#     for a, b in pairwise(contexts, None):
#         end = -1 if b is None else b.original_index
#         yield SectionContext(
#             a.section_name,
#             a.previous_line,
#             a.line,
#             lines[a.original_index + 1 : end],
#             a.original_index,
#             b is None,
#         )


# def _check_numpy_sections(self, lines, definition, docstring):
#     """NumPy-style docstring sections checks.

#     Check the general format of a sectioned docstring:
#         '''This is my one-liner.

#         Short Summary
#         -------------
#         This is my summary.

#         Returns
#         -------
#         None.

#         '''

#     Section names appear in `NUMPY_SECTION_NAMES`.
#     Yields all violation from `_check_numpy_section` for each valid
#     Numpy-style section.
#     """
#     found_any_numpy_section = False
#     for ctx in self._get_section_contexts(lines, self.NUMPY_SECTION_NAMES):
#         found_any_numpy_section = True
#         yield from self._check_numpy_section(docstring, definition, ctx)

#     return found_any_numpy_section


# def _check_google_sections(self, lines, definition, docstring):
#     """Google-style docstring section checks.

#     Check the general format of a sectioned docstring:
#         '''This is my one-liner.

#         Note:
#             This is my summary.

#         Returns:
#             None.

#         '''

#     Section names appear in `GOOGLE_SECTION_NAMES`.
#     Yields all violation from `_check_google_section` for each valid
#     Google-style section.
#     """
#     for ctx in self._get_section_contexts(lines, self.GOOGLE_SECTION_NAMES):
#         yield from self._check_google_section(docstring, definition, ctx)


# @check(Definition)
# def check_docstring_sections(self, definition, docstring, config):
#     """Check for docstring sections."""
#     if not docstring:
#         return

#     lines = docstring.split("\n")
#     if len(lines) < 2:
#         return

#     found_numpy = yield from self._check_numpy_sections(
#         lines, definition, docstring
#     )
#     if not found_numpy:
#         yield from self._check_google_sections(lines, definition, docstring)

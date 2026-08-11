"""Read an SSH config content to extract tokens."""

import re
from dataclasses import dataclass

from ssh_config_ls.exceptions import (
    BadConfigurationOptionError,
    NoArgumentAfterKeywordError,
    SSHConfigError,
)
from ssh_config_ls.keywords import Keyword

# ------------------------------------------------------------
# CLASSES
# ------------------------------------------------------------


@dataclass(frozen=True)
class KeywordArgToken:
    """Token of a keyword-argument line."""

    line_number: int
    """Line number in the document."""
    keyword: Keyword
    """Token representing the keyword of the line."""
    args: list[str]
    """Token representing the arguments of the line."""
    comment: str | None = None
    """Token representing inline comment if presents."""


LineToken = KeywordArgToken | str
"""Token of a non-empty line in SSH config."""


# ------------------------------------------------------------
# PUBLIC FUNCTIONS
# ------------------------------------------------------------


def tokenize(content: str) -> list[LineToken]:
    """Read a SSH config content to extract tokens.

    Args:
        content: The content of an SSH config file.

    Returns:
        All keyword-argument lines from the content read as tokens.
    """
    token_list = []
    for i, line in enumerate(content.splitlines()):
        if line.strip() == "":
            continue
        if _is_standalone_comment(line):
            token_list.append(line.strip())
        else:
            token_list.append(_split_line(line, i))
    return token_list


def tokenize_with_errors(content: str) -> tuple[list[LineToken], list[SSHConfigError]]:
    """Read a SSH config content to extract tokens.

    Args:
        content: The content of an SSH config file.

    Returns:
        All keyword-argument lines from the content read as tokens.
    """
    token_list, errors = [], []
    for i, line in enumerate(content.splitlines()):
        if line.strip() == "":
            continue
        if _is_standalone_comment(line):
            token_list.append(line.strip())
        else:
            try:
                token_list.append(_split_line(line, i))
            except SSHConfigError as e:
                errors.append(e)
    return token_list, errors


# ------------------------------------------------------------
# PRIVATE FUNCTIONS
# ------------------------------------------------------------


def _is_standalone_comment(line: str) -> bool:
    """Check if the line is a comment.

    As explained in the [`ssh_config`](https://man.openbsd.org/ssh_config) manual:
    Lines starting with # and empty lines are interpreted as comments.

    We choose to consider that only lines with # as first non-whitespace character
        as a standalone comment and so tokenized.
    """
    return line.lstrip()[0] == "#"


def _split_line(line: str, line_number: int) -> KeywordArgToken:
    """Split a line as a keyword-argument pair.

    Args:
        line: A keyword-argument line from an SSH config.
        line_number: Line number in the source configuration file.

    Returns:
        The line as a `Keyword`-argument token.
    """
    words = re.split(r"\s*=\s*|\s+", line.lstrip(), maxsplit=1)

    try:
        keyword = Keyword(words[0].lower())
    except ValueError as e:
        match = re.search(r"\S+", line)
        positions = (match.start(), match.end())  # ty: ignore[unresolved-attribute]
        raise BadConfigurationOptionError(line_number, positions, words[0]) from e

    try:
        arg_line = words[1]
    except IndexError as e:
        positions = (len(line) - 1, len(line) - 1)
        raise NoArgumentAfterKeywordError(line_number, positions) from e

    match keyword:
        case Keyword.LOCALCOMMAND | Keyword.PROXYCOMMAND | Keyword.REMOTECOMMAND:
            args = [arg_line.strip()]
            inline_comment = None
        case _:
            args, inline_comment = _split_argument(arg_line)

    if len(args) == 0:
        positions = (len(line) - 1, len(line) - 1)
        raise NoArgumentAfterKeywordError(line_number, positions)

    return KeywordArgToken(line_number, keyword, args, inline_comment)


def _split_argument(rest_of_line: str) -> tuple[list[str], str | None]:
    """Split an argument from an SSH config line.

    Args:
        rest_of_line: The argument part of an SSH config line.

    Returns:
        Arguments split by whitespace, except when quoted.
    """
    args = []
    argument = ""
    inline_comment = None
    in_quote = False
    for i, ch in enumerate(rest_of_line):
        if ch == "#" and not in_quote:
            inline_comment = rest_of_line[i:].strip()
            break
        if ch == " " and not in_quote:
            argument = argument.strip().strip('"')
            if argument != "":
                args.append(argument)
                argument = ""
            continue
        if ch == '"':
            in_quote = not in_quote
        argument += ch

    argument = argument.strip().strip('"')
    if argument != "":
        args.append(argument)

    return args, inline_comment

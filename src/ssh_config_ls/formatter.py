"""Write a formatted SSH config from a syntax tree."""

import re
from functools import partial
from typing import Final
lazy from collections.abc import Sequence

from ssh_config_ls.keywords import Keyword
from ssh_config_ls.lexer import KeywordArgToken
from ssh_config_ls.parser import GlobalBlock, HostBlock, MatchBlock, SSHBlock, SSHConfig

# ------------------------------------------------------------
# CONSTANTS
# ------------------------------------------------------------

DEFAULT_INDENT: Final[str] = "    "
"""Default indent for Host and Match blocks directives."""
DEFAULT_SEPARATOR: Final[str] = " "
"""Default separator between a keyword and its arguments."""

# ------------------------------------------------------------
# PUBLIC FUNCTIONS
# ------------------------------------------------------------


def format_tree(
    tree: SSHConfig,
    /,
    *,
    indent: str = DEFAULT_INDENT,
    separator: str = DEFAULT_SEPARATOR,
) -> str:
    """Format an SSH config syntax tree as a string.

    Args:
        tree: The syntax tree of the SSH config.
        indent: Indentation applied to directives inside a block.
        separator: Separator between keywords and their arguments.

    Returns:
        The formatted SSH config as a string.
    """
    if not re.fullmatch(r"\s*", indent):
        msg = f"Invalid indent {indent!r}: must contain only whitespace."
        raise ValueError(msg)

    if not re.fullmatch(r"\s*=\s*|\s+", separator):
        msg = f"Invalid separator {separator!r}: must be whitespace or '='."
        raise ValueError(msg)

    return "\n\n".join(
        [
            _format_block(block, indent=indent, separator=separator)
            for block in tree.blocks
            if len(block.directives) > 0
        ]
    )


# ------------------------------------------------------------
# PRIVATE FUNCTIONS
# ------------------------------------------------------------


def _format_block(
    block: SSHBlock,
    /,
    *,
    indent: str = DEFAULT_INDENT,
    separator: str = DEFAULT_SEPARATOR,
) -> str:
    """Format an SSH config syntax block as a string.

    Args:
        block: A syntax block of the SSH config.
        indent: Indentation applied to directives inside the block.
        separator: Separator between keywords and their arguments.

    Returns:
        The formatted SSH config block as a string.
    """
    indent_used = "" if isinstance(block, GlobalBlock) else indent
    formatted_lines: list[str] = []
    if isinstance(block, HostBlock):
        formatted_lines.append(
            _write_keyword_argument_line(
                Keyword.HOST, block.patterns, block.comment, indent=""
            )
        )
    elif isinstance(block, MatchBlock):
        formatted_lines.append(
            _write_keyword_argument_line(
                Keyword.MATCH, (block.conditions), block.comment, indent=""
            )
        )
    for line in block.directives:
        if isinstance(line, KeywordArgToken):
            formatted_lines.append(
                _write_keyword_argument_line(
                    line.keyword,
                    line.args,
                    line.comment,
                    indent=indent_used,
                    separator=separator,
                )
            )
        else:
            formatted_lines.append(f"{indent_used}{line}")
    return "\n".join(formatted_lines)


def _write_keyword_argument_line(
    keyword: Keyword,
    args: Sequence[str],
    comment: str | None,
    /,
    *,
    indent: str = DEFAULT_INDENT,
    separator: str = DEFAULT_SEPARATOR,
) -> str:
    """Write a keyword-argument line of an SSH config.

    Args:
        keyword: The keyword of the directive.
        args: Arguments associated with the keyword.
        comment: Inline comment to append, if any.
        indent: Indentation prefix applied to the line.
        separator: Separator between the keyword and its arguments.

    Returns:
        The formatted line as a string.
    """
    line = (
        f"{indent}{keyword.value.canonical}{separator}"
        f"{' '.join(map(partial(_quote_arg_if_needed, keyword), args))}"
    )
    if comment:
        line += f" {comment}"
    return line


def _quote_arg_if_needed(keyword: Keyword, arg: str) -> str:
    """Quote an argument if it contains whitespace.

    Arguments for LocalCommand, ProxyCommand, and RemoteCommand are never
    quoted as they are shell commands interpreted verbatim by OpenSSH.

    Args:
        keyword: Keyword the argument belongs to.
        arg: Argument to potentially quote.

    Returns:
        The argument wrapped in double quotes if it contains whitespace,
        unchanged otherwise.
    """
    if keyword not in (
        Keyword.LOCALCOMMAND,
        Keyword.PROXYCOMMAND,
        Keyword.REMOTECOMMAND,
    ) and (" " in arg or arg[0] == "="):
        return f'"{arg}"'
    return arg

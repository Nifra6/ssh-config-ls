"""Write a formatted SSH config from a syntax tree."""

from collections.abc import Sequence
from functools import partial

from ssh_config_ls.lexer import Keyword, KeywordArgToken
from ssh_config_ls.parser import GlobalBlock, HostBlock, MatchBlock, SSHConfig

# ------------------------------------------------------------
# PUBLIC FUNCTIONS
# ------------------------------------------------------------


def format_tree(
    tree: SSHConfig, /, *, indent: str = "    ", separator: str = " "
) -> str:
    """Format an SSH config syntax tree as a string.

    Args:
        tree: The syntax tree of the SSH config.
        indent: Indentation applied to directives inside a block.
        separator: Separator between keywords and their arguments.

    Returns:
        The formatted SSH config as a string.
    """
    formatted_blocks: list[str] = []

    for block in tree.blocks:
        indent_used = "" if isinstance(block, GlobalBlock) else indent
        formatted_lines: list[str] = []
        if isinstance(block, HostBlock):
            formatted_lines.append(
                _write_keyword_argument_line(
                    Keyword.Host, block.patterns, block.comment
                )
            )
        elif isinstance(block, MatchBlock):
            formatted_lines.append(
                _write_keyword_argument_line(
                    Keyword.Match, (block.conditions), block.comment
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
        formatted_blocks.append("\n".join(formatted_lines))

    return "\n\n".join(formatted_blocks) + "\n"


# ------------------------------------------------------------
# PRIVATE FUNCTIONS
# ------------------------------------------------------------


def _write_keyword_argument_line(
    keyword: Keyword,
    args: Sequence[str],
    comment: str | None,
    /,
    *,
    indent: str = "",
    separator: str = " ",
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
        f"{indent}{keyword.name}{separator}"
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
    if (
        keyword
        not in (Keyword.LocalCommand, Keyword.ProxyCommand, Keyword.RemoteCommand)
        and " " in arg
    ):
        return f'"{arg}"'
    return arg

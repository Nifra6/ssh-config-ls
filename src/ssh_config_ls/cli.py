"""CLI of SSH-config-ls."""

from pathlib import Path
from typing import Annotated

import typer
from rich import print as rich_print

from ssh_config_ls import __version__
from ssh_config_ls.exceptions import SSHConfigError
from ssh_config_ls.formatter import DEFAULT_INDENT, DEFAULT_SEPARATOR
from ssh_config_ls.parser import DEFAULT_SORT

# ------------------------------------------------------------
# APPLICATION
# ------------------------------------------------------------

app = typer.Typer(
    help="An SSH config formatter, usable as a Language Server Protocol (LSP) plugin.",
    no_args_is_help=True,
)

# ------------------------------------------------------------
# COMMANDS
# ------------------------------------------------------------


@app.command(name="format", no_args_is_help=True)
def cli_format_config(
    files: Annotated[
        list[Path], typer.Argument(help="List of config files to format.")
    ],
    indent: Annotated[
        str, typer.Option(help="Indentation applied to directives inside a block.")
    ] = DEFAULT_INDENT,
    separator: Annotated[
        str, typer.Option(help="Separator between keywords and their arguments.")
    ] = DEFAULT_SEPARATOR,
    sort_directives: Annotated[
        bool, typer.Option(help="Sort directives within blocks.")
    ] = DEFAULT_SORT,
) -> None:
    """Format an SSH config file."""
    from ssh_config_ls.formatter import format_tree
    from ssh_config_ls.lexer import tokenize
    from ssh_config_ls.parser import parse

    formatted_files = 0
    unchanged_files = 0
    for file in files:
        content = file.read_text()

        try:
            tokens = tokenize(content)
            syntax_tree = parse(tokens, sort_directives=sort_directives)
            formatted_content = format_tree(
                syntax_tree, indent=indent, separator=separator
            )

            if content != formatted_content:
                formatted_files += 1
                with file.open("w") as f:
                    f.write(formatted_content)
            else:
                unchanged_files += 1
        except SSHConfigError:
            unchanged_files += 1
            continue

    if formatted_files > 0 and unchanged_files > 0:
        rich_print(
            f"{formatted_files} file{'s' if formatted_files > 1 else ''} formatted,"
            f" {unchanged_files} file{'s' if unchanged_files > 1 else ''} unchanged."
        )
    elif formatted_files > 0:
        rich_print(
            f"{formatted_files} file{'s' if formatted_files > 1 else ''} formatted."
        )
    else:
        rich_print(
            f"{unchanged_files} file{'s' if unchanged_files > 1 else ''} unchanged."
        )


@app.command(name="server")
def cli_start_server() -> None:
    """Start the SSH config language server."""
    from ssh_config_ls.lsp import server

    server.start_io()


@app.command(name="version")
def cli_version() -> None:
    """Display sshls's version."""
    rich_print(__version__)

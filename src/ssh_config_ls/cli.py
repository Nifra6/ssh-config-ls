"""CLI of SSH-config-ls."""

from pathlib import Path
from typing import Annotated

import typer

from ssh_config_ls.formatter import DEFAULT_INDENT, DEFAULT_SEPARATOR

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
    file: Annotated[Path, typer.Argument(help="Path to the config file.")],
    indent: Annotated[
        str, typer.Option(help="Indentation applied to directives inside a block.")
    ] = DEFAULT_INDENT,
    separator: Annotated[
        str, typer.Option(help="Separator between keywords and their arguments.")
    ] = DEFAULT_SEPARATOR,
) -> None:
    """Format an SSH config file."""
    from ssh_config_ls.formatter import format_tree
    from ssh_config_ls.lexer import tokenize
    from ssh_config_ls.parser import parse

    content = file.read_text()

    tokens = tokenize(content)
    syntax_tree = parse(tokens)
    formatted_content = format_tree(syntax_tree, indent=indent, separator=separator)

    with file.open("w") as f:
        f.write(formatted_content)


@app.command(name="server")
def cli_start_server() -> None:
    """Start the SSH config language server."""
    from ssh_config_ls.lsp import server

    server.start_io()

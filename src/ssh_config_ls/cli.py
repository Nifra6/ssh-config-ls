"""CLI of SSH-config-ls."""

from pathlib import Path
from typing import Annotated

import typer

# ------------------------------------------------------------
# APPLICATION
# ------------------------------------------------------------

app = typer.Typer()

# ------------------------------------------------------------
# COMMANDS
# ------------------------------------------------------------


@app.command(name="format")
def cli_format_config(
    file: Annotated[Path, typer.Argument(help="Path to the config file.")],
) -> None:
    """Format an SSH config file."""
    from ssh_config_ls.formatter import format_tree
    from ssh_config_ls.lexer import tokenize
    from ssh_config_ls.parser import parse

    content = file.read_text()

    tokens = tokenize(content)
    syntax_tree = parse(tokens)
    formatted_content = format_tree(syntax_tree)

    with file.open("w") as f:
        f.write(formatted_content)


@app.command(name="server")
def cli_start_server() -> None:
    """Start the SSH config language server."""
    raise NotImplementedError

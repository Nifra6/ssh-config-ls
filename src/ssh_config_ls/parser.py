"""Construct a syntax tree from the tokens of an SSH config."""

from collections.abc import Sequence
from dataclasses import dataclass

from ssh_config_ls.tokenizer import Keyword, KeywordArgToken, LineToken

# ------------------------------------------------------------
# CLASSES
# ------------------------------------------------------------


Directive = KeywordArgToken | str
"""A directive in an SSH config block, or a standalone comment."""


@dataclass(frozen=True)
class GlobalBlock:
    """Block applied as a fallback to every destination."""

    directives: tuple[Directive, ...]


@dataclass(frozen=True)
class HostBlock:
    """Block applied to hosts matching the given patterns."""

    patterns: tuple[str, ...]
    directives: tuple[Directive, ...]
    comment: str | None = None


@dataclass(frozen=True)
class MatchBlock:
    """Block applied when the given conditions are met."""

    conditions: str
    directives: tuple[Directive, ...]
    comment: str | None = None


@dataclass(frozen=True)
class SSHConfig:
    """Syntax tree representing an SSH configuration."""

    blocks: tuple[GlobalBlock | HostBlock | MatchBlock, ...] = (GlobalBlock(()),)


# ------------------------------------------------------------
# PUBLIC FUNCTIONS
# ------------------------------------------------------------


def parse(tokens: Sequence[LineToken]) -> SSHConfig:
    """Construct a syntax tree from the tokens of an SSH config.

    Args:
        tokens: Tokens representing lines of an SSH config.

    Returns:
        The syntax tree of the SSH config.
    """
    blocks = []
    current_block: KeywordArgToken | None = None
    current_directives: list[LineToken] = []

    for tok in tokens:
        if isinstance(tok, str):
            current_directives.append(tok)
        elif tok.keyword in (Keyword.Host, Keyword.Match):
            blocks.append(_flush_block(current_block, current_directives))
            current_directives = []
            current_block = tok
        else:
            current_directives.append(tok)
    blocks.append(_flush_block(current_block, current_directives))

    return SSHConfig(tuple(blocks))


# ------------------------------------------------------------
# PRIVATE FUNCTIONS
# ------------------------------------------------------------


def _flush_block(
    block_definition: KeywordArgToken | None, directives: Sequence[LineToken]
) -> GlobalBlock | HostBlock | MatchBlock:
    """Construct a syntax block from an SSH config block.

    Args:
        block_definition: Host or Match keyword-argument delimiting the block.
            None if it is the global block of the config.
        directives: Keyword-argument tokens and standalone comments
            belonging to the block.

    Returns:
        The syntax block representing the structure of the config block.
    """
    if block_definition is None:
        return GlobalBlock(tuple(directives))

    if block_definition.keyword == Keyword.Host:
        return HostBlock(
            tuple(block_definition.args),
            tuple(directives),
            comment=block_definition.comment,
        )

    if block_definition.keyword == Keyword.Match:
        return MatchBlock(
            " ".join(block_definition.args),
            tuple(directives),
            comment=block_definition.comment,
        )

    msg = f"Expected Host or Match keyword, got {block_definition.keyword}"
    raise ValueError(msg)

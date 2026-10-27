"""Construct a syntax tree from the tokens of an SSH config."""

from dataclasses import dataclass
from typing import Final
lazy from collections.abc import Sequence

from ssh_config_ls.keywords import Keyword
from ssh_config_ls.lexer import KeywordArgToken, LineToken

# ------------------------------------------------------------
# CONSTANTS
# ------------------------------------------------------------

DEFAULT_SORT: Final[bool] = True
"""Sort blocks directives by default."""


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


SSHBlock = GlobalBlock | HostBlock | MatchBlock
"""Block in a SSH config."""


@dataclass(frozen=True)
class SSHConfig:
    """Syntax tree representing an SSH configuration."""

    blocks: tuple[SSHBlock, ...] = (GlobalBlock(()),)


# ------------------------------------------------------------
# PUBLIC FUNCTIONS
# ------------------------------------------------------------


def parse(
    tokens: Sequence[LineToken], /, *, sort_directives: bool = DEFAULT_SORT
) -> SSHConfig:
    """Construct a syntax tree from the tokens of an SSH config.

    Args:
        tokens: Tokens representing lines of an SSH config.
        sort_directives: Sort directives within parsed blocks.

    Returns:
        The syntax tree of the SSH config.
    """
    blocks = []
    current_block: KeywordArgToken | None = None
    current_directives: list[LineToken] = []

    for tok in tokens:
        if isinstance(tok, str):
            current_directives.append(tok)
        elif tok.keyword in (Keyword.HOST, Keyword.MATCH):
            blocks.append(
                _flush_block(
                    current_block, current_directives, sort_directives=sort_directives
                )
            )
            current_directives = []
            current_block = tok
        else:
            current_directives.append(tok)
    blocks.append(
        _flush_block(current_block, current_directives, sort_directives=sort_directives)
    )

    return SSHConfig(tuple(blocks))


# ------------------------------------------------------------
# PRIVATE FUNCTIONS
# ------------------------------------------------------------


def _flush_block(
    block_definition: KeywordArgToken | None,
    directives: Sequence[LineToken],
    /,
    *,
    sort_directives: bool = True,
) -> SSHBlock:
    """Construct a syntax block from an SSH config block.

    Args:
        block_definition: Host or Match keyword-argument delimiting the block.
            None if it is the global block of the config.
        directives: Keyword-argument tokens and standalone comments
            belonging to the block.
        sort_directives: Sort directives in the block.

    Returns:
        The syntax block representing the structure of the config block.
    """
    sort = _sort_directives if sort_directives else tuple

    if block_definition is None:
        return GlobalBlock(sort(directives))

    if block_definition.keyword == Keyword.HOST:
        return HostBlock(
            tuple(block_definition.args),
            sort(directives),
            comment=block_definition.comment,
        )

    if block_definition.keyword == Keyword.MATCH:
        return MatchBlock(
            " ".join(block_definition.args),
            sort(directives),
            comment=block_definition.comment,
        )

    msg = f"Expected Host or Match keyword, got {block_definition.keyword}"
    raise ValueError(msg)


def _sort_directives(directives: Sequence[Directive]) -> tuple[Directive, ...]:
    """Sort directives by keyword order if no standalone comment is present.

    Args:
        directives: Sequence of directive tokens (keyword-argument lines or
            standalone comments) from a parsed block.

    Returns:
        The directives sorted by keyword declaration order if no standalone
        comment is present, otherwise the original sequence as a tuple.
    """
    if not any(isinstance(line, str) for line in directives):
        keyword_order = list(Keyword)
        return tuple(sorted(directives, key=lambda k: keyword_order.index(k.keyword)))  # ty: ignore[unresolved-attribute]
    return tuple(directives)

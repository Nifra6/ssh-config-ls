# ruff: noqa: S101,D103  # noqa: INP001
"""Unit tests of the formatter."""

import pytest

from ssh_config_ls.formatter import format_tree
from ssh_config_ls.lexer import Keyword, KeywordArgToken
from ssh_config_ls.parser import GlobalBlock, HostBlock, SSHConfig

# ------------------------------------------------------------
# CONSTANTS
# ------------------------------------------------------------

EXEMPLES: list[tuple[SSHConfig, str]] = [
    (SSHConfig(), ""),
    (
        SSHConfig(
            (
                GlobalBlock(
                    (
                        KeywordArgToken(Keyword.IdentityFile, ["/home/user/my key"]),
                        KeywordArgToken(Keyword.User, ["secret_user"]),
                    )
                ),
            )
        ),
        """IdentityFile "/home/user/my key"
User secret_user""",
    ),
    (
        SSHConfig(
            (
                GlobalBlock((KeywordArgToken(Keyword.Port, ["22"]),)),
                HostBlock(
                    ("myserver",),
                    (KeywordArgToken(Keyword.Hostname, ["192.168.1.1"]),),
                    comment="# inline comment",
                ),
            )
        ),
        """Port 22

Host myserver # inline comment
    Hostname 192.168.1.1""",
    ),
]

# ------------------------------------------------------------
# HAPPY PATH
# ------------------------------------------------------------


@pytest.mark.parametrize(("tree", "expected"), EXEMPLES)
def test_classic_trees(tree: SSHConfig, expected: str) -> None:
    assert format_tree(tree) == expected


# ------------------------------------------------------------
# ERROR HANDLING
# ------------------------------------------------------------


@pytest.mark.parametrize("indent", ["  la  ", " = ", "~~"])
def test_incorrect_indent(indent: str) -> None:
    with pytest.raises(
        ValueError, match=f"Invalid indent {indent!r}: must contain only whitespace."
    ):
        format_tree(EXEMPLES[0][0], indent=indent)


@pytest.mark.parametrize("separator", ["  ==  ", "    : ", "<-"])
def test_incorrect_separator(separator: str) -> None:
    with pytest.raises(
        ValueError, match=f"Invalid separator {separator!r}: must be whitespace or '='."
    ):
        format_tree(EXEMPLES[0][0], separator=separator)


# ------------------------------------------------------------
# IDEMPOTENCY
# ------------------------------------------------------------


@pytest.mark.parametrize(("tree", "_"), EXEMPLES)
def test_idempotent(tree: SSHConfig, _: str) -> None:
    assert format_tree(tree) == format_tree(tree)

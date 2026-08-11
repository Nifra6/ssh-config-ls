# ruff: noqa: S101,D103  # noqa: INP001
"""Unit tests of the parser."""

import pytest

from ssh_config_ls.keywords import Keyword
from ssh_config_ls.lexer import KeywordArgToken, LineToken
from ssh_config_ls.parser import GlobalBlock, HostBlock, SSHConfig, parse

# ------------------------------------------------------------
# CONSTANTS
# ------------------------------------------------------------

EXEMPLES: list[tuple[list[LineToken], SSHConfig]] = [
    ([], SSHConfig()),
    (
        [
            KeywordArgToken(0, Keyword.IDENTITYFILE, ["/home/user/my key"]),
            KeywordArgToken(1, Keyword.USER, ["secret_user"]),
        ],
        SSHConfig(
            (
                GlobalBlock(
                    (
                        KeywordArgToken(0, Keyword.IDENTITYFILE, ["/home/user/my key"]),
                        KeywordArgToken(1, Keyword.USER, ["secret_user"]),
                    )
                ),
            )
        ),
    ),
    (
        [
            KeywordArgToken(0, Keyword.PORT, ["22"]),
            KeywordArgToken(1, Keyword.HOST, ["myserver"], comment="# inline comment"),
            KeywordArgToken(2, Keyword.HOSTNAME, ["192.168.1.1"]),
        ],
        SSHConfig(
            (
                GlobalBlock((KeywordArgToken(0, Keyword.PORT, ["22"]),)),
                HostBlock(
                    ("myserver",),
                    (KeywordArgToken(2, Keyword.HOSTNAME, ["192.168.1.1"]),),
                    comment="# inline comment",
                ),
            )
        ),
    ),
]


# ------------------------------------------------------------
# HAPPY PATH
# ------------------------------------------------------------


@pytest.mark.parametrize(("tokens", "expected"), EXEMPLES)
def test_classic_configurations(tokens: list[LineToken], expected: SSHConfig) -> None:
    assert parse(tokens) == expected


# ------------------------------------------------------------
# IDEMPOTENCY
# ------------------------------------------------------------


@pytest.mark.parametrize(("tokens", "_"), EXEMPLES)
def test_idempotent(tokens: list[LineToken], _: SSHConfig) -> None:
    assert parse(tokens) == parse(tokens)

# ruff: noqa: S101,D103  # noqa: INP001
"""Unit tests of the parser."""

import pytest

from ssh_config_ls.lexer import Keyword, KeywordArgToken, LineToken
from ssh_config_ls.parser import GlobalBlock, HostBlock, SSHConfig, parse

# ------------------------------------------------------------
# CONSTANTS
# ------------------------------------------------------------

EXEMPLES: list[tuple[list[LineToken], SSHConfig]] = [
    ([], SSHConfig()),
    (
        [
            KeywordArgToken(0, Keyword.IdentityFile, ["/home/user/my key"]),
            KeywordArgToken(1, Keyword.User, ["secret_user"]),
        ],
        SSHConfig(
            (
                GlobalBlock(
                    (
                        KeywordArgToken(0, Keyword.IdentityFile, ["/home/user/my key"]),
                        KeywordArgToken(1, Keyword.User, ["secret_user"]),
                    )
                ),
            )
        ),
    ),
    (
        [
            KeywordArgToken(0, Keyword.Port, ["22"]),
            KeywordArgToken(1, Keyword.Host, ["myserver"], comment="# inline comment"),
            KeywordArgToken(2, Keyword.Hostname, ["192.168.1.1"]),
        ],
        SSHConfig(
            (
                GlobalBlock((KeywordArgToken(0, Keyword.Port, ["22"]),)),
                HostBlock(
                    ("myserver",),
                    (KeywordArgToken(2, Keyword.Hostname, ["192.168.1.1"]),),
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

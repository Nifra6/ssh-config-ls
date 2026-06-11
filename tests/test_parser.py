# ruff: noqa: S101,D103  # noqa: INP001
"""Unit tests of the parser."""

import pytest

from ssh_config_ls.lexer import Keyword, KeywordArgToken, LineToken
from ssh_config_ls.parser import GlobalBlock, HostBlock, SSHConfig, parse

# ------------------------------------------------------------
# HAPPY PATH
# ------------------------------------------------------------


@pytest.mark.parametrize(
    ("tokens", "expected"),
    [
        ([], SSHConfig()),
        (
            [
                KeywordArgToken(Keyword.IdentityFile, ["/home/user/my key"]),
                KeywordArgToken(Keyword.User, ["secret_user"]),
            ],
            SSHConfig(
                (
                    GlobalBlock(
                        (
                            KeywordArgToken(
                                Keyword.IdentityFile, ["/home/user/my key"]
                            ),
                            KeywordArgToken(Keyword.User, ["secret_user"]),
                        )
                    ),
                )
            ),
        ),
        (
            [
                KeywordArgToken(Keyword.Port, ["22"]),
                KeywordArgToken(Keyword.Host, ["myserver"], comment="# inline comment"),
                KeywordArgToken(Keyword.Hostname, ["192.168.1.1"]),
            ],
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
        ),
    ],
)
def test_classic_configurations(tokens: list[LineToken], expected: SSHConfig) -> None:
    assert parse(tokens) == expected

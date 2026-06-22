# ruff: noqa: S101,D103  # noqa: INP001
"""Unit tests of the formatter."""

import pytest

from ssh_config_ls.formatter import format_tree
from ssh_config_ls.lexer import Keyword, KeywordArgToken
from ssh_config_ls.parser import GlobalBlock, HostBlock, SSHConfig

# ------------------------------------------------------------
# HAPPY PATH
# ------------------------------------------------------------


@pytest.mark.parametrize(
    ("tree", "expected"),
    [
        (SSHConfig(), ""),
        (
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
    ],
)
def test_classic_trees(tree: SSHConfig, expected: str) -> None:
    assert format_tree(tree) == expected

# ruff: noqa: S101,D103  # noqa: INP001
"""Unit tests of the tokenizer."""

import pytest

from ssh_config_ls.exceptions import (
    BadConfigurationOptionError,
    NoArgumentAfterKeywordError,
)
from ssh_config_ls.lexer import Keyword, KeywordArgToken, LineToken, tokenize

# ------------------------------------------------------------
# CONSTANTS
# ------------------------------------------------------------

SINGLE_LINE_CASES: list[tuple[str, list[LineToken]]] = [
    ("", []),
    ("# An awesome comment", ["# An awesome comment"]),
    ("  HostName 192.168.1.1", [KeywordArgToken(0, Keyword.Hostname, ["192.168.1.1"])]),
    ("Port = 22", [KeywordArgToken(0, Keyword.Port, ["22"])]),
    (
        "Host myserver # inline comment",
        [KeywordArgToken(0, Keyword.Host, ["myserver"], comment="# inline comment")],
    ),
]

# ------------------------------------------------------------
# HAPPY PATH
# ------------------------------------------------------------


@pytest.mark.parametrize(("line", "expected"), SINGLE_LINE_CASES)
def test_single_line(line: str, expected: list[LineToken]) -> None:
    assert tokenize(line) == expected


@pytest.mark.parametrize("line", ["Port=22", "Port =22", "Port= 22", "Port = 22"])
def test_equals_separator(line: str) -> None:
    token = tokenize(line)
    assert token[0] == KeywordArgToken(0, Keyword.Port, ["22"])


def test_quoted_value() -> None:
    tokens = tokenize('IdentityFile "/home/user/my key"')
    assert KeywordArgToken(0, Keyword.IdentityFile, ["/home/user/my key"]) in tokens


@pytest.mark.parametrize(
    ("line", "comment"),
    [
        ("Host myserver # inline comment", "# inline comment"),
        ("Host myserver# comment without space", "# comment without space"),
    ],
)
def test_inline_comment_preserved(line: str, comment: str) -> None:
    token = tokenize(line)[0]
    assert isinstance(token, KeywordArgToken)
    assert token.args == ["myserver"]
    assert token.comment == comment


# ------------------------------------------------------------
# EDGE CASES
# ------------------------------------------------------------


@pytest.mark.parametrize("line", [" ", "\t", "  \t  \t"])
def test_blank_variants(line: str) -> None:
    assert tokenize(line) == []


@pytest.mark.parametrize("line", ["  Host foo", "\tHost foo", "Host   foo"])
def test_whitespace_tolerance(line: str) -> None:
    token = tokenize(line)[0]
    assert isinstance(token, KeywordArgToken)
    assert token.args == ["foo"]


@pytest.mark.parametrize("raw", ["host", "HOST", "hOsT", "HoSt"])
def test_keyword_case_insensitive(raw: str) -> None:
    token = tokenize(f"{raw} myserver")[0]
    assert isinstance(token, KeywordArgToken)
    assert token.keyword is Keyword.Host


@pytest.mark.parametrize(
    ("line", "keyword"),
    [("ipqos lowdelay", Keyword.IPQoS), ("macs hmac-sha2-256", Keyword.MACs)],
)
def test_awkward_case_keywords(line: str, keyword: Keyword) -> None:
    token = tokenize(line)[0]
    assert isinstance(token, KeywordArgToken)
    assert token.keyword is keyword


def test_host_multiple_patterns() -> None:
    token = tokenize("Host bastion jumpbox")[0]
    assert isinstance(token, KeywordArgToken)
    assert token.keyword == Keyword.Host
    assert token.args == ["bastion", "jumpbox"]


@pytest.mark.parametrize(
    ("line", "expected_value"),
    [
        ("IdentityFile ~/.ssh/id_rsa", ["~/.ssh/id_rsa"]),
        ("IdentityFile /home/user/.ssh", ["/home/user/.ssh"]),
        ("ProxyCommand ssh -W %h:%p bastion", ["ssh -W %h:%p bastion"]),
        ("ControlPath /tmp/ssh-%r@%h:%p", ["/tmp/ssh-%r@%h:%p"]),  # noqa: S108
    ],
)
def test_special_characters_in_value(line: str, expected_value: list[str]) -> None:
    token = tokenize(line)[0]
    assert isinstance(token, KeywordArgToken)
    assert token.args == expected_value


def test_include_glob() -> None:
    tokens = tokenize("Include ~/.ssh/conf.d/*.conf")
    assert tokens[0] == KeywordArgToken(0, Keyword.Include, ["~/.ssh/conf.d/*.conf"])


@pytest.mark.parametrize(
    ("line", "expected_value"),
    [
        ("Host *.example.com", ["*.example.com"]),
        ("Host bastion?", ["bastion?"]),
        ("Host 192.168.1.*", ["192.168.1.*"]),
    ],
)
def test_wildcard_values(line: str, expected_value: list[str]) -> None:
    token = tokenize(line)[0]
    assert isinstance(token, KeywordArgToken)
    assert token.args == expected_value


@pytest.mark.parametrize("line", ['hosTname "yes # lol" #rofl'])
def test_inline_comment_and_quoted_hash(line: str) -> None:
    token = tokenize(line)[0]
    assert isinstance(token, KeywordArgToken)
    assert token.args == ["yes # lol"]
    assert token.comment == "#rofl"


# ------------------------------------------------------------
# ERROR HANDLING
# ------------------------------------------------------------


def test_keyword_without_value() -> None:
    with pytest.raises(NoArgumentAfterKeywordError):
        tokenize("Host")


def test_unknown_keyword() -> None:
    with pytest.raises(BadConfigurationOptionError):
        tokenize("UnknownKeyword value")


# ------------------------------------------------------------
# IDEMPOTENCY
# ------------------------------------------------------------


@pytest.mark.parametrize(("line", "_"), SINGLE_LINE_CASES)
def test_idempotent(line: str, _: list[LineToken]) -> None:
    assert tokenize(line) == tokenize(line)


# ------------------------------------------------------------
# CONTRACT
# ------------------------------------------------------------


def test_returns_list() -> None:
    assert isinstance(tokenize("Host foo"), list)


def test_token_types() -> None:
    for token in tokenize("Host foo\n# comment"):
        assert isinstance(token, LineToken)


@pytest.mark.parametrize(("line", "_"), SINGLE_LINE_CASES[2:])
def test_keyword_arg_token_fields(line: str, _: list[LineToken]) -> None:
    token = tokenize(line)[0]
    assert hasattr(token, "keyword")
    assert isinstance(token.keyword, Keyword)
    assert hasattr(token, "args")
    assert isinstance(token.args, list)
    for arg in token.args:
        assert isinstance(arg, str)
    assert hasattr(token, "comment")
    assert isinstance(token.comment, str | None)

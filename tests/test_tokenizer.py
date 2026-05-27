# ruff: noqa: S101,D103  # noqa: INP001
"""Unit tests of the tokenizer."""

import pytest

from ssh_config_ls.exceptions import (
    BadConfigurationOptionError,
    NoArgumentAfterKeywordError,
)
from ssh_config_ls.tokenizer import Keyword, LineToken, tokenize


@pytest.mark.parametrize(
    ("line", "expected"),
    [
        ("Host myserver", [(Keyword.Host, ["myserver"])]),
        ("  HostName 192.168.1.1", [(Keyword.Hostname, ["192.168.1.1"])]),
        ("Port 22", [(Keyword.Port, ["22"])]),
        ("", []),
        ("# commentaire", []),
    ],
)
def test_single_line(line: str, expected: LineToken) -> None:
    assert tokenize(line) == expected


@pytest.mark.parametrize("line", ["  Host foo", "\tHost foo", "Host   foo"])
def test_whitespace_tolerance(line: str) -> None:
    assert tokenize(line)[0][1] == ["foo"]


def test_empty_input() -> None:
    assert tokenize("") == []


def test_only_whitespace() -> None:
    assert tokenize("   \t  ") == []


def test_value_with_spaces() -> None:
    tokens = tokenize('IdentityFile "/home/user/my key"')
    assert (Keyword.IdentityFile, ["/home/user/my key"]) in tokens


@pytest.mark.parametrize("raw", ["host", "HOST", "hOsT", "HoSt"])
def test_keyword_case_insensitive(raw: str) -> None:
    tokens = tokenize(f"{raw} myserver")
    assert tokens[0][0] is Keyword.Host


def test_keyword_without_value() -> None:
    with pytest.raises(NoArgumentAfterKeywordError):
        tokenize("Host")


def test_unknown_keyword() -> None:
    with pytest.raises(BadConfigurationOptionError):
        tokenize("UnknownKeyword value")


@pytest.mark.parametrize(
    "line", ["Host myserver # commentaire inline", "Host myserver# sans espace"]
)
def test_inline_comment_stripped(line: str) -> None:
    tokens = tokenize(line)
    assert tokens[0][1] == ["myserver"]


@pytest.mark.parametrize("line", ['hosTname "oui # haha" #pouet'])
def test_inline_comment_and_quoted_hash(line: str) -> None:
    tokens = tokenize(line)
    assert tokens[0][1] == ["oui # haha"]


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
    tokens = tokenize(line)
    assert tokens[0][1] == expected_value


@pytest.mark.parametrize(
    ("line", "expected_value"),
    [
        ("Host *.example.com", ["*.example.com"]),
        ("Host bastion?", ["bastion?"]),
        ("Host 192.168.1.*", ["192.168.1.*"]),
    ],
)
def test_wildcard_values(line: str, expected_value: list[str]) -> None:
    tokens = tokenize(line)
    assert tokens[0][1] == expected_value


def test_host_multiple_patterns() -> None:
    tokens = tokenize("Host bastion jumpbox")
    assert tokens[0][0] is Keyword.Host
    assert tokens[0][1][0] == "bastion"
    assert tokens[0][1][1] == "jumpbox"


@pytest.mark.parametrize(
    ("line", "keyword"),
    [("ipqos lowdelay", Keyword.IPQoS), ("macs hmac-sha2-256", Keyword.MACs)],
)
def test_awkward_case_keywords(line: str, keyword: Keyword) -> None:
    tokens = tokenize(line)
    assert tokens[0][0] is keyword


@pytest.mark.parametrize("line", [" ", "\t", "  \t  \t"])
def test_blank_variants(line: str) -> None:
    assert tokenize(line) == []


@pytest.mark.parametrize("line", ["Port=22", "Port =22", "Port= 22", "Port = 22"])
def test_equals_separator(line: str) -> None:
    tokens = tokenize(line)
    assert tokens[0] == (Keyword.Port, ["22"])


def test_include_glob() -> None:
    tokens = tokenize("Include ~/.ssh/conf.d/*.conf")
    assert tokens[0] == (Keyword.Include, ["~/.ssh/conf.d/*.conf"])

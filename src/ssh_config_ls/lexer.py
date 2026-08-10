"""Read an SSH config content to extract tokens."""

import re
from dataclasses import dataclass
from enum import StrEnum, auto

from ssh_config_ls.exceptions import (
    BadConfigurationOptionError,
    NoArgumentAfterKeywordError,
    SSHConfigError,
)

# ------------------------------------------------------------
# CLASSES
# ------------------------------------------------------------


class Keyword(StrEnum):
    """Keyword tokens used in SSH configs."""

    Host = auto()
    Match = auto()
    AddKeysToAgent = auto()
    AddressFamily = auto()
    BatchMode = auto()
    BindAddress = auto()
    BindInterface = auto()
    CanonicalDomains = auto()
    CanonicalizeFallbackLocal = auto()
    CanonicalizeHostname = auto()
    CanonicalizeMaxDots = auto()
    CanonicalizePermittedCNAMEs = auto()
    CASignatureAlgorithms = auto()
    CertificateFile = auto()
    ChannelTimeout = auto()
    CheckHostIP = auto()
    Ciphers = auto()
    ClearAllForwardings = auto()
    Compression = auto()
    ConnectionAttempts = auto()
    ConnectTimeout = auto()
    ControlMaster = auto()
    ControlPath = auto()
    ControlPersist = auto()
    DynamicForward = auto()
    EnableEscapeCommandline = auto()
    EnableSSHKeysign = auto()
    EscapeChar = auto()
    ExitOnForwardFailure = auto()
    FingerprintHash = auto()
    ForkAfterAuthentification = auto()
    ForwardAgent = auto()
    ForwardX11 = auto()
    ForwardX11Timeout = auto()
    ForwardX11Trusted = auto()
    GatewayPorts = auto()
    GlobalKnownHostsFile = auto()
    GSSAPIAuthentification = auto()
    GSSAPIDelegateCredentials = auto()
    HashKnownHosts = auto()
    HostbasedAcceptedAlgorithms = auto()
    HostbasedAuthentification = auto()
    HostKeyAlgorithms = auto()
    HostKeyAlias = auto()
    Hostname = auto()
    IdentitiesOnly = auto()
    IdentityAgent = auto()
    IdentityFile = auto()
    IgnoreUnknown = auto()
    Include = auto()
    IPQoS = auto()
    KbdInteractiveAuthentication = auto()
    KbdInteractiveDevices = auto()
    KexAlgorithms = auto()
    KnownHostsCommand = auto()
    LocalCommand = auto()
    LocalForward = auto()
    LogLevel = auto()
    LogVerbose = auto()
    MACs = auto()
    NoHostAuthenticationForLocalhost = auto()
    NumberOfPasswordPrompts = auto()
    ObscureKeystrokeTiming = auto()
    PasswordAuthentication = auto()
    PermitLocalCommand = auto()
    PermitRemoteOpen = auto()
    PKCS11Provider = auto()
    Port = auto()
    PreferredAuthentications = auto()
    ProxyCommand = auto()
    ProxyJump = auto()
    ProxyUseFdpass = auto()
    PubkeyAcceptedAlgorithms = auto()
    PubkeyAuthentication = auto()
    RefuseConnection = auto()
    RekeyLimit = auto()
    RemoteCommand = auto()
    RemoteForward = auto()
    RequestTTY = auto()
    RequiredRSASize = auto()
    RevokedHostKeys = auto()
    SecurityKeyProvider = auto()
    SendEnv = auto()
    ServerAliveCountMax = auto()
    ServerAliveInterval = auto()
    SessionType = auto()
    SetEnv = auto()
    StdinNull = auto()
    StreamLocalBindMask = auto()
    StreamLocalBindUnlink = auto()
    StrictHostKeyChecking = auto()
    SyslogFacility = auto()
    TCKeepAlive = auto()
    Tag = auto()
    Tunnel = auto()
    TunnelDevice = auto()
    UpdateHostKeys = auto()
    User = auto()
    UserKnownHostsFile = auto()
    VerifyHostKeyDNS = auto()
    VersionAddendum = auto()
    VisualHostKey = auto()
    WarnWeakCrypto = auto()
    XAuthLocation = auto()


@dataclass(frozen=True)
class KeywordArgToken:
    """Token of a keyword-argument line."""

    line_number: int
    """Line number in the document."""
    keyword: Keyword
    """Token representing the keyword of the line."""
    args: list[str]
    """Token representing the arguments of the line."""
    comment: str | None = None
    """Token representing inline comment if presents."""


LineToken = KeywordArgToken | str
"""Token of a non-empty line in SSH config."""


# ------------------------------------------------------------
# PUBLIC FUNCTIONS
# ------------------------------------------------------------


def tokenize(content: str) -> list[LineToken]:
    """Read a SSH config content to extract tokens.

    Args:
        content: The content of an SSH config file.

    Returns:
        All keyword-argument lines from the content read as tokens.
    """
    token_list = []
    for i, line in enumerate(content.splitlines()):
        if line.strip() == "":
            continue
        if _is_standalone_comment(line):
            token_list.append(line.strip())
        else:
            token_list.append(_split_line(line, i))
    return token_list


def tokenize_with_errors(content: str) -> tuple[list[LineToken], list[SSHConfigError]]:
    """Read a SSH config content to extract tokens.

    Args:
        content: The content of an SSH config file.

    Returns:
        All keyword-argument lines from the content read as tokens.
    """
    token_list, errors = [], []
    for i, line in enumerate(content.splitlines()):
        if line.strip() == "":
            continue
        if _is_standalone_comment(line):
            token_list.append(line.strip())
        else:
            try:
                token_list.append(_split_line(line, i))
            except SSHConfigError as e:
                errors.append(e)
    return token_list, errors


# ------------------------------------------------------------
# PRIVATE FUNCTIONS
# ------------------------------------------------------------


def _is_standalone_comment(line: str) -> bool:
    """Check if the line is a comment.

    As explained in the [`ssh_config`](https://man.openbsd.org/ssh_config) manual:
    Lines starting with # and empty lines are interpreted as comments.

    We choose to consider that only lines with # as first non-whitespace character
        as a standalone comment and so tokenized.
    """
    return line.lstrip()[0] == "#"


def _split_line(line: str, line_number: int) -> KeywordArgToken:
    """Split a line as a keyword-argument pair.

    Args:
        line: A keyword-argument line from an SSH config.
        line_number: Line number in the source configuration file.

    Returns:
        The line as a `Keyword`-argument token.
    """
    words = re.split(r"\s*=\s*|\s+", line.lstrip(), maxsplit=1)

    try:
        keyword = Keyword(words[0].lower())
    except ValueError as e:
        match = re.search(r"\S+", line)
        positions = (match.start(), match.end())  # ty: ignore[unresolved-attribute]
        raise BadConfigurationOptionError(line_number, positions, words[0]) from e

    try:
        arg_line = words[1]
    except IndexError as e:
        positions = (len(line) - 1, len(line) - 1)
        raise NoArgumentAfterKeywordError(line_number, positions) from e

    match keyword:
        case Keyword.LocalCommand | Keyword.ProxyCommand | Keyword.RemoteCommand:
            args = [arg_line.strip()]
            inline_comment = None
        case _:
            args, inline_comment = _split_argument(arg_line)

    if len(args) == 0:
        positions = (len(line) - 1, len(line) - 1)
        raise NoArgumentAfterKeywordError(line_number, positions)

    return KeywordArgToken(line_number, keyword, args, inline_comment)


def _split_argument(rest_of_line: str) -> tuple[list[str], str | None]:
    """Split an argument from an SSH config line.

    Args:
        rest_of_line: The argument part of an SSH config line.

    Returns:
        Arguments split by whitespace, except when quoted.
    """
    args = []
    argument = ""
    inline_comment = None
    in_quote = False
    for i, ch in enumerate(rest_of_line):
        if ch == "#" and not in_quote:
            inline_comment = rest_of_line[i:].strip()
            break
        if ch == " " and not in_quote:
            argument = argument.strip().strip('"')
            if argument != "":
                args.append(argument)
                argument = ""
            continue
        if ch == '"':
            in_quote = not in_quote
        argument += ch

    argument = argument.strip().strip('"')
    if argument != "":
        args.append(argument)

    return args, inline_comment

"""Read an SSH config content to extract tokens."""

import re
from enum import StrEnum, auto

from ssh_config_ls.exceptions import (
    BadConfigurationOptionError,
    NoArgumentAfterKeywordError,
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


LineToken = tuple[Keyword, list[str]]
"""Token of a `Keyword`-argument line."""

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
    for line in content.splitlines():
        if _is_comment(line):
            continue
        token_list.append(_split_line(line))
    return token_list


# ------------------------------------------------------------
# PRIVATE FUNCTIONS
# ------------------------------------------------------------


def _is_comment(line: str) -> bool:
    """Check if the line is a comment.

    As explained in the [ssh_config](https://man.openbsd.org/ssh_config) manual:
    Lines starting with # and empty lines are interpreted as comments.
    """
    return line[0] == "#" or line.lstrip() == ""


def _split_line(line: str) -> LineToken:
    """Split a line as a keyword-argument pair.

    Args:
        line: A keyword-argument line from an SSH config.

    Returns:
        The line as a `Keyword`-argument token.
    """
    words = re.split(r"\s*=\s*|\s+", line.lstrip(), maxsplit=1)

    try:
        keyword = Keyword(words[0].lower())
    except ValueError as e:
        raise BadConfigurationOptionError from e

    try:
        arg_line = words[1]
    except IndexError as e:
        raise NoArgumentAfterKeywordError from e

    match keyword:
        case Keyword.LocalCommand | Keyword.ProxyCommand | Keyword.RemoteCommand:
            args = [arg_line.strip()]
        case _:
            args = _split_argument(arg_line)

    if len(args) == 0:
        raise NoArgumentAfterKeywordError

    return (keyword, args)


def _split_argument(rest_of_line: str) -> list[str]:
    """Split an argument from an SSH config line.

    Args:
        rest_of_line: The argument part of an SSH config line.

    Returns:
        Arguments split by whitespace, except when quoted.
    """
    args = []
    argument = ""
    in_quote = False
    for ch in rest_of_line:
        if ch == "#" and not in_quote:
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

    return args

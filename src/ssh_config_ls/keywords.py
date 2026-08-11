"""Representation of SSH config keywords."""

from dataclasses import dataclass
from enum import Enum
from typing import Self

# ------------------------------------------------------------
# CLASSES
# ------------------------------------------------------------


@dataclass(frozen=True)
class KeywordDef:
    """Keyword definition and properties of an SSH config keyword."""

    canonical: str

    def __str__(self) -> str:
        """Return the canonical name of the Keyword."""
        return self.canonical


class Keyword(Enum):
    """Keyword tokens used in SSH configs."""

    HOST = KeywordDef("Host")
    MATCH = KeywordDef("Match")
    ADDKEYSTOAGENT = KeywordDef("AddKeysToAgent")
    ADDRESSFAMILY = KeywordDef("AddressFamily")
    BATCHMODE = KeywordDef("BatchMode")
    BINDADDRESS = KeywordDef("BindAddress")
    BINDINTERFACE = KeywordDef("BindInterface")
    CANONICALDOMAINS = KeywordDef("CanonicalDomains")
    CANONICALIZEFALLBACKLOCAL = KeywordDef("CanonicalizeFallbackLocal")
    CANONICALIZEHOSTNAME = KeywordDef("CanonicalizeHostname")
    CANONICALIZEMAXDOTS = KeywordDef("CanonicalizeMaxDots")
    CANONICALIZEPERMITTEDCNAMES = KeywordDef("CanonicalizePermittedCNAMEs")
    CASIGNATUREALGORITHMS = KeywordDef("CASignatureAlgorithms")
    CERTIFICATEFILE = KeywordDef("CertificateFile")
    CHANNELTIMEOUT = KeywordDef("ChannelTimeout")
    CHECKHOSTIP = KeywordDef("CheckHostIP")
    CIPHERS = KeywordDef("Ciphers")
    CLEARALLFORWARDINGS = KeywordDef("ClearAllForwardings")
    COMPRESSION = KeywordDef("Compression")
    CONNECTIONATTEMPTS = KeywordDef("ConnectionAttempts")
    CONNECTTIMEOUT = KeywordDef("ConnectTimeout")
    CONTROLMASTER = KeywordDef("ControlMaster")
    CONTROLPATH = KeywordDef("ControlPath")
    CONTROLPERSIST = KeywordDef("ControlPersist")
    DYNAMICFORWARD = KeywordDef("DynamicForward")
    ENABLEESCAPECOMMANDLINE = KeywordDef("EnableEscapeCommandline")
    ENABLESSHKEYSIGN = KeywordDef("EnableSSHKeysign")
    ESCAPECHAR = KeywordDef("EscapeChar")
    EXITONFORWARDFAILURE = KeywordDef("ExitOnForwardFailure")
    FINGERPRINTHASH = KeywordDef("FingerprintHash")
    FORKAFTERAUTHENTIFICATION = KeywordDef("ForkAfterAuthentification")
    FORWARDAGENT = KeywordDef("ForwardAgent")
    FORWARDX11 = KeywordDef("ForwardX11")
    FORWARDX11TIMEOUT = KeywordDef("ForwardX11Timeout")
    FORWARDX11TRUSTED = KeywordDef("ForwardX11Trusted")
    GATEWAYPORTS = KeywordDef("GatewayPorts")
    GLOBALKNOWNHOSTSFILE = KeywordDef("GlobalKnownHostsFile")
    GSSAPIAUTHENTIFICATION = KeywordDef("GSSAPIAuthentification")
    GSSAPIDELEGATECREDENTIALS = KeywordDef("GSSAPIDelegateCredentials")
    HASHKNOWNHOSTS = KeywordDef("HashKnownHosts")
    HOSTBASEDACCEPTEDALGORITHMS = KeywordDef("HostbasedAcceptedAlgorithms")
    HOSTBASEDAUTHENTIFICATION = KeywordDef("HostbasedAuthentification")
    HOSTKEYALGORITHMS = KeywordDef("HostKeyAlgorithms")
    HOSTKEYALIAS = KeywordDef("HostKeyAlias")
    HOSTNAME = KeywordDef("Hostname")
    IDENTITIESONLY = KeywordDef("IdentitiesOnly")
    IDENTITYAGENT = KeywordDef("IdentityAgent")
    IDENTITYFILE = KeywordDef("IdentityFile")
    IGNOREUNKNOWN = KeywordDef("IgnoreUnknown")
    INCLUDE = KeywordDef("Include")
    IPQOS = KeywordDef("IPQoS")
    KBDINTERACTIVEAUTHENTICATION = KeywordDef("KbdInteractiveAuthentication")
    KBDINTERACTIVEDEVICES = KeywordDef("KbdInteractiveDevices")
    KEXALGORITHMS = KeywordDef("KexAlgorithms")
    KNOWNHOSTSCOMMAND = KeywordDef("KnownHostsCommand")
    LOCALCOMMAND = KeywordDef("LocalCommand")
    LOCALFORWARD = KeywordDef("LocalForward")
    LOGLEVEL = KeywordDef("LogLevel")
    LOGVERBOSE = KeywordDef("LogVerbose")
    MACS = KeywordDef("MACs")
    NOHOSTAUTHENTICATIONFORLOCALHOST = KeywordDef("NoHostAuthenticationForLocalhost")
    NUMBEROFPASSWORDPROMPTS = KeywordDef("NumberOfPasswordPrompts")
    OBSCUREKEYSTROKETIMING = KeywordDef("ObscureKeystrokeTiming")
    PASSWORDAUTHENTICATION = KeywordDef("PasswordAuthentication")
    PERMITLOCALCOMMAND = KeywordDef("PermitLocalCommand")
    PERMITREMOTEOPEN = KeywordDef("PermitRemoteOpen")
    PKCS11PROVIDER = KeywordDef("PKCS11Provider")
    PORT = KeywordDef("Port")
    PREFERREDAUTHENTICATIONS = KeywordDef("PreferredAuthentications")
    PROXYCOMMAND = KeywordDef("ProxyCommand")
    PROXYJUMP = KeywordDef("ProxyJump")
    PROXYUSEFDPASS = KeywordDef("ProxyUseFdpass")
    PUBKEYACCEPTEDALGORITHMS = KeywordDef("PubkeyAcceptedAlgorithms")
    PUBKEYAUTHENTICATION = KeywordDef("PubkeyAuthentication")
    REFUSECONNECTION = KeywordDef("RefuseConnection")
    REKEYLIMIT = KeywordDef("RekeyLimit")
    REMOTECOMMAND = KeywordDef("RemoteCommand")
    REMOTEFORWARD = KeywordDef("RemoteForward")
    REQUESTTTY = KeywordDef("RequestTTY")
    REQUIREDRSASIZE = KeywordDef("RequiredRSASize")
    REVOKEDHOSTKEYS = KeywordDef("RevokedHostKeys")
    SECURITYKEYPROVIDER = KeywordDef("SecurityKeyProvider")
    SENDENV = KeywordDef("SendEnv")
    SERVERALIVECOUNTMAX = KeywordDef("ServerAliveCountMax")
    SERVERALIVEINTERVAL = KeywordDef("ServerAliveInterval")
    SESSIONTYPE = KeywordDef("SessionType")
    SETENV = KeywordDef("SetEnv")
    STDINNULL = KeywordDef("StdinNull")
    STREAMLOCALBINDMASK = KeywordDef("StreamLocalBindMask")
    STREAMLOCALBINDUNLINK = KeywordDef("StreamLocalBindUnlink")
    STRICTHOSTKEYCHECKING = KeywordDef("StrictHostKeyChecking")
    SYSLOGFACILITY = KeywordDef("SyslogFacility")
    TCKEEPALIVE = KeywordDef("TCKeepAlive")
    TAG = KeywordDef("Tag")
    TUNNEL = KeywordDef("Tunnel")
    TUNNELDEVICE = KeywordDef("TunnelDevice")
    UPDATEHOSTKEYS = KeywordDef("UpdateHostKeys")
    USER = KeywordDef("User")
    USERKNOWNHOSTSFILE = KeywordDef("UserKnownHostsFile")
    VERIFYHOSTKEYDNS = KeywordDef("VerifyHostKeyDNS")
    VERSIONADDENDUM = KeywordDef("VersionAddendum")
    VISUALHOSTKEY = KeywordDef("VisualHostKey")
    WARNWEAKCRYPTO = KeywordDef("WarnWeakCrypto")
    XAUTHLOCATION = KeywordDef("XAuthLocation")

    @classmethod
    def _missing_(cls, value) -> Self | None:  # noqa: ANN001
        value = value.lower()
        for member in cls:
            if member.value.canonical.lower() == value:
                return member
        return None

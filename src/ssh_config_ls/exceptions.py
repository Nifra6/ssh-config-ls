"""Exceptions raised by the SSH config LS."""


class SSHConfigError(ValueError):
    """Base class for SSH config parsing errors."""


class BadConfigurationOptionError(SSHConfigError):
    """The given keyword does not exist in the specification."""


class NoArgumentAfterKeywordError(SSHConfigError):
    """No argument has been given with the keyword."""

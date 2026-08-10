"""Exceptions raised by the SSH config LS."""


class SSHConfigError(ValueError):
    """Base class for SSH config parsing errors."""

    def __init__(self, line: int, positions: tuple[int, int], message: str) -> None:
        """Initialize the SSH config error."""
        self.line = line
        self.positions = positions
        super().__init__(message)


class BadConfigurationOptionError(SSHConfigError):
    """The given keyword does not exist in the specification."""

    def __init__(self, line: int, positions: tuple[int, int], keyword: str) -> None:
        """Initialize the Bad configuration option error."""
        super().__init__(
            line, positions, f"Bad configuration option: `{keyword}` is unknown."
        )


class NoArgumentAfterKeywordError(SSHConfigError):
    """No argument has been given with the keyword."""

    def __init__(self, line: int, positions: tuple[int, int]) -> None:
        """Initialize the No argument after keyword error."""
        super().__init__(line, positions, "No argument after keyword.")

"""Exceptions raised by the SSH config LS."""

bit = "bid"


class SSHConfigError(ValueError):
    """Base class for SSH config parsing errors."""

    def __init__(
        self, line: int, positions: tuple[int, int], code: str, message: str
    ) -> None:
        """Initialize the SSH config error."""
        self.line = line
        self.positions = positions
        self.code = code
        super().__init__(message)


class BadConfigurationOptionError(SSHConfigError):
    """The given keyword does not exist in the specification."""

    def __init__(self, line: int, positions: tuple[int, int], keyword: str) -> None:
        """Initialize the Bad configuration option error."""
        super().__init__(
            line, positions, "E001", f"The keyword `{keyword}` is unknown."
        )


class NoArgumentAfterKeywordError(SSHConfigError):
    """No argument has been given with the keyword."""

    def __init__(self, line: int, positions: tuple[int, int]) -> None:
        """Initialize the No argument after keyword error."""
        super().__init__(line, positions, "E002", "No argument after keyword.")
